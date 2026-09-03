from pathlib import Path


def main() -> None:
    workflow = (
        Path(__file__).resolve().parents[1]
        / ".github/workflows/classic-gcc12.yml"
    ).read_text()

    assert workflow.index("- name: Checkout CMaNGOS Classic") < workflow.index(
        "- name: Checkout Playerbots"
    )
    assert "path: mangos/src/modules/PlayerBots" in workflow
    assert "make -C mangos/src/modules/PlayerBots test" in workflow
    assert (
        'FETCHCONTENT_SOURCE_DIR_PLAYERBOTS="$GITHUB_WORKSPACE/mangos/src/modules/PlayerBots"'
        in workflow
    )


if __name__ == "__main__":
    main()
