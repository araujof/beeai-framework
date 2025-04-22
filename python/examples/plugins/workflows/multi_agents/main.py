import asyncio
import sys
import traceback

from beeai_framework.backend import ChatModel
from beeai_framework.emitter import EmitterOptions
from beeai_framework.errors import FrameworkError
from beeai_framework.workflows import AgentWorkflow
from examples.helpers.io import ConsoleReader


async def main() -> None:
    workflow = AgentWorkflow(name="Smart assistant")

    workflow.add_plugin(
        name="Researcher",
    )

    workflow.add_plugin(
        name="WeatherForecaster",
    )

    workflow.add_plugin(
        name="DataSynthesizer",
    )

    reader = ConsoleReader()

    reader.write("Assistant 🤖 : ", "What location do you want to learn about?")
    for prompt in reader:
        await (
            workflow.run({"location": prompt})
            .on(
                # Event Matcher -> match agent's 'success' events
                lambda event: isinstance(event.creator, ChatModel) and event.name == "success",
                # log data to the console
                lambda data, event: reader.write(
                    "->Got response from the LLM",
                    "  \n->".join([str(message.content[0].model_dump()) for message in data.value.messages]),
                ),
                EmitterOptions(match_nested=True),
            )
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
