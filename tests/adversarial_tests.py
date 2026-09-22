"""Live injected-email evaluation through the current ticket pipeline."""
from tests.live_checks import run

if __name__ == '__main__':
    raise SystemExit(run(adversarial=True))
