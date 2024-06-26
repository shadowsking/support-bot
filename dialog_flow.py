import argparse
import json
import os
from typing import Tuple

import dotenv
from google.cloud import dialogflow


def detect_intent_by_text(
    project_id, session_id, text, language_code=None
) -> tuple[bool, str]:
    """
    Returns the result of detect intent with text as input.

    Using the same `session_id` between requests allows continuation
    of the conversation.
    """

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return (
        response.query_result.intent.is_fallback,
        response.query_result.fulfillment_text,
    )


def create_intent(
    project_id, display_name, training_phrases_parts, message_texts
) -> None:
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def learn_intents_by_json(project_id, path) -> None:
    with open(path, "r", encoding="utf-8") as f:
        questions = json.load(f)
        for name, data in questions.items():
            create_intent(
                project_id=project_id,
                display_name=name,
                training_phrases_parts=data["questions"],
                message_texts=[data["answer"]],
            )


if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser(description="Create new intents from json file")
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="The path to the json file with the questions",
        default="questions.json",
    )
    args = parser.parse_args()

    learn_intents_by_json(project_id=os.environ["GOOGLE_CLOUD_PROJECT"], path=args.file)
