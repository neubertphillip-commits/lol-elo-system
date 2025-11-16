"""
Tournament Context ELO Variant
Uses different K-factors based on tournament importance
Higher stakes tournaments = higher K-factor = bigger rating changes
"""

from typing import Dict, Optional
from variants.with_dynamic_offsets import DynamicOffsetElo


class TournamentContextElo(DynamicOffsetElo):
    """
    ELO system with tournament-context-aware K-factors

    Rationale:
    - Worlds/MSI: Highest stakes, teams prepare more → bigger swings (K=32)
    - Playoffs: High stakes → moderate increase (K=28)
    - Regular Season: Standard stakes → baseline (K=24)
    - First Stand/Low tier: Lower stakes → reduced (K=20)
    """

    # Tournament-specific K-factors
    TOURNAMENT_K_FACTORS = {
        # International tournaments (highest stakes)
        'worlds': 32,
        'world_championship': 32,
        'msi': 32,
        'mid-season_invitational': 32,

        # Playoffs (high stakes)
        'playoffs': 28,
        'finals': 28,
        'championship': 28,

        # Regular season (baseline)
        'regular_season': 24,
        'regular': 24,

        # Lower stakes
        'first_stand': 20,
        'promotion': 20,
    }

    def __init__(self, k_factor: float = 24, initial_elo: float = 1500,
                 use_scale_factors: bool = True, scale_factors: Dict = None):
        """
        Initialize Tournament Context ELO

        Args:
            k_factor: Baseline K-factor (used if tournament not recognized)
            initial_elo: Starting ELO rating
            use_scale_factors: Whether to use match closeness adjustments
            scale_factors: Scale factor configuration
        """
        super().__init__(k_factor, initial_elo, use_scale_factors, scale_factors)
        self.baseline_k = k_factor

    def get_tournament_k_factor(self, tournament: Optional[str], stage: Optional[str]) -> float:
        """
        Determine K-factor based on tournament and stage

        Args:
            tournament: Tournament name
            stage: Tournament stage (e.g., "Playoffs", "Regular Season")

        Returns:
            Appropriate K-factor
        """
        # Normalize strings
        tournament_lower = str(tournament).lower() if tournament else ""
        stage_lower = str(stage).lower() if stage else ""

        # Check tournament name first
        for keyword, k_factor in self.TOURNAMENT_K_FACTORS.items():
            if keyword in tournament_lower:
                return k_factor

        # Check stage
        for keyword, k_factor in self.TOURNAMENT_K_FACTORS.items():
            if keyword in stage_lower:
                return k_factor

        # Default to baseline
        return self.baseline_k

    def update_ratings(self, team1: str, team2: str, score1: int, score2: int,
                       tournament: Optional[str] = None, stage: Optional[str] = None,
                       **kwargs):
        """
        Update ratings with tournament context

        Args:
            team1: First team name
            team2: Second team name
            score1: First team score
            score2: Second team score
            tournament: Tournament name
            stage: Tournament stage
            **kwargs: Additional parameters
        """
        # Get context-appropriate K-factor
        k_factor = self.get_tournament_k_factor(tournament, stage)

        # Temporarily override K-factor
        original_k = self.k_factor
        self.k_factor = k_factor

        try:
            # Call parent's update_ratings
            super().update_ratings(team1, team2, score1, score2, **kwargs)
        finally:
            # Restore original K-factor
            self.k_factor = original_k

    def get_match_importance(self, tournament: Optional[str], stage: Optional[str]) -> str:
        """
        Get human-readable importance level

        Args:
            tournament: Tournament name
            stage: Tournament stage

        Returns:
            Importance level string
        """
        k_factor = self.get_tournament_k_factor(tournament, stage)

        if k_factor >= 32:
            return "Highest (International)"
        elif k_factor >= 28:
            return "High (Playoffs)"
        elif k_factor >= 24:
            return "Standard (Regular Season)"
        else:
            return "Low (Lower Tier)"


if __name__ == "__main__":
    # Test the tournament context system
    print("="*70)
    print("TOURNAMENT CONTEXT ELO - TEST")
    print("="*70)

    elo = TournamentContextElo()

    # Test different tournament contexts
    test_cases = [
        ("LEC 2024 Summer", "Regular Season", "T1", "Gen.G", 2, 1),
        ("LEC 2024 Summer", "Playoffs", "T1", "Gen.G", 3, 2),
        ("World Championship 2024", "Knockout", "T1", "Gen.G", 3, 1),
        ("MSI 2024", "Finals", "T1", "Gen.G", 3, 0),
        ("First Stand 2024", "Regular", "Team A", "Team B", 1, 0),
    ]

    print("\n📊 Testing K-Factor Assignment:\n")
    print(f"{'Tournament':<30} {'Stage':<20} {'K-Factor':<10} {'Importance':<25}")
    print("-"*85)

    for tournament, stage, t1, t2, s1, s2 in test_cases:
        k_factor = elo.get_tournament_k_factor(tournament, stage)
        importance = elo.get_match_importance(tournament, stage)

        print(f"{tournament:<30} {stage:<20} {k_factor:<10.0f} {importance:<25}")

    # Simulate a season with mixed tournaments
    print("\n" + "="*70)
    print("SIMULATION: TEAM RATING CHANGES BY TOURNAMENT TYPE")
    print("="*70)

    elo = TournamentContextElo()

    # Start both teams at 1500
    print("\nInitial Ratings:")
    print(f"  T1: {elo.get_rating('T1'):.0f}")
    print(f"  Gen.G: {elo.get_rating('Gen.G'):.0f}")

    # Regular season win
    print("\n1. Regular Season: T1 beats Gen.G 2-1")
    elo.update_ratings('T1', 'Gen.G', 2, 1,
                      tournament="LEC 2024 Summer", stage="Regular Season")
    print(f"  T1: {elo.get_rating('T1'):.0f} (change: +{elo.get_rating('T1') - 1500:.0f})")
    print(f"  Gen.G: {elo.get_rating('Gen.G'):.0f} (change: {elo.get_rating('Gen.G') - 1500:.0f})")

    # Reset
    elo.ratings = {'T1': 1500.0, 'Gen.G': 1500.0}

    # Playoffs win
    print("\n2. Playoffs: T1 beats Gen.G 3-2")
    elo.update_ratings('T1', 'Gen.G', 3, 2,
                      tournament="LEC 2024 Summer", stage="Playoffs")
    print(f"  T1: {elo.get_rating('T1'):.0f} (change: +{elo.get_rating('T1') - 1500:.0f})")
    print(f"  Gen.G: {elo.get_rating('Gen.G'):.0f} (change: {elo.get_rating('Gen.G') - 1500:.0f})")

    # Reset
    elo.ratings = {'T1': 1500.0, 'Gen.G': 1500.0}

    # Worlds win
    print("\n3. Worlds Finals: T1 beats Gen.G 3-1")
    elo.update_ratings('T1', 'Gen.G', 3, 1,
                      tournament="World Championship 2024", stage="Finals")
    print(f"  T1: {elo.get_rating('T1'):.0f} (change: +{elo.get_rating('T1') - 1500:.0f})")
    print(f"  Gen.G: {elo.get_rating('Gen.G'):.0f} (change: {elo.get_rating('Gen.G') - 1500:.0f})")

    print("\n💡 Notice: Worlds produces bigger rating changes than regular season!")
