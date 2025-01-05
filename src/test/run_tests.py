from src.core.main import main
from src.test.test_scenarios import create_test_scenario_1, create_test_scenario_2

def run_all_tests():
    """Run all test scenarios."""
    test_params = [
        {
            "name": "high_congestion_scenario",
            "scenario": create_test_scenario_1,
            "params": (20, 5, 0.7, 0.3, [0, 10], [5, 14])
        },
        {
            "name": "hotspot_scenario",
            "scenario": create_test_scenario_2,
            "params": (20, 5, 0.7, 0.3, [0, 10], [5, 14])
        }
    ]
    
    for test in test_params:
        print(f"\nRunning {test['name']}...")
        try:
            main(*test['params'], test_scenario=test['scenario'], test_name=test['name'])
            print(f"{test['name']} completed successfully")
        except Exception as e:
            print(f"{test['name']} failed: {str(e)}")

if __name__ == "__main__":
    run_all_tests()
