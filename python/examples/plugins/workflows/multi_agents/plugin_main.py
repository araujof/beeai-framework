import asyncio
import sys
import traceback

from beeai_framework.errors import FrameworkError
from beeai_framework.plugins.types import PluggableRegistry
from examples.helpers.io import ConsoleReader


async def main() -> None:
    registry = PluggableRegistry(config="./config.yaml")

    loc_agent = registry.lookup("LocationAgent")

    reader = ConsoleReader()

    reader.write("Assistant 🤖 : ", "What location do you want to learn about?")
    for prompt in reader:
        await (
            loc_agent.run({"location": prompt})
            .on(
                "success",
                lambda data, event: reader.write(
                    f"->Step '{data.step}' has been completed with the following outcome."
                    f"\n\n{data.state.final_answer}\n\n",
                    data.model_dump(exclude={"data"}),
                ),
            )
        )
        reader.write("Assistant 🤖 : ", "What location do you want to learn about?")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
