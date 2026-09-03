"""The LLM debug output must not expose the full HTTP request."""

from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "playerbot/PlayerbotLLMInterface.cpp"


def main() -> None:
    source = SOURCE.read_text()

    debug_writes = [
        line for line in source.splitlines() if "debugLines.push_back" in line
    ]
    assert all("requestStr" not in line for line in debug_writes)
    assert '"Send HTTP request: POST " + parsedUrl.path' in source
    assert 'std::to_string(body.size()) + " bytes"' in source


if __name__ == "__main__":
    main()
