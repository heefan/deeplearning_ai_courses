import autogen
import utils

SEO_REVIEWER = autogen.AssistantAgent(
    name="SEO Reviewer",
    system_message="You are an SEO reviewer, known for "
    "your ability to optimize content for search engines, "
    "ensuring that it ranks well and attracts organic traffic. "
    "Make sure your suggestion is concise (within 3 bullet points), "
    "concrete and to the point. "
    "Begin the review by stating your role.",
)

LEGAL_REVIEWER = autogen.AssistantAgent(
    name="Legal Reviewer",
    llm_config=utils.llm_config(),
    system_message="You are a legal reviewer, known for "
    "your ability to ensure that content is legally compliant "
    "and free from any potential legal issues. "
    "Make sure your suggestion is concise (within 3 bullet points), "
    "concrete and to the point. "
    "Begin the review by stating your role.",
)

ETHICS_REVIEWER = autogen.AssistantAgent(
    name="Ethics Reviewer",
    llm_config=utils.llm_config(),
    system_message="You are an ethics reviewer, known for "
    "your ability to ensure that content is ethically sound "
    "and free from any potential ethical issues. "
    "Make sure your suggestion is concise (within 3 bullet points), "
    "concrete and to the point. "
    "Begin the review by stating your role. ",
)

META_REVIEWER = autogen.AssistantAgent(
    name="Meta Reviewer",
    llm_config=utils.llm_config(),
    system_message="You are a meta reviewer, you aggragate and review "
    "the work of other reviewers and give a final suggestion on the content.",
)


### Private Orchestrate all the agent to solve the task ###
def _reflection_message(recipient, message, sender, config):
    return f"""Review the following content:
    \n\n {recipient.chat_messages_for_summary(sender)[-1]["content"]}"""


_review_chats = [
    {
        "recipient": SEO_REVIEWER,
        "message": _reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return review into as JSON object only:"
            "{'Reviewer': '', 'Review': ''}. Here Reviewer should be your role",
        },
        "max_turns": 1,
    },
    {
        "recipient": LEGAL_REVIEWER,
        "message": _reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return review into as JSON object only:"
            "{'Reviewer': '', 'Review': ''}.",
        },
        "max_turns": 1,
    },
    {
        "recipient": ETHICS_REVIEWER,
        "message": _reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return review into as JSON object only:"
            "{'reviewer': '', 'review': ''}",
        },
        "max_turns": 1,
    },
    {
        "recipient": META_REVIEWER,
        "message": "Aggregate feedback from all reviewers and give final suggestions on the writing.",
        "max_turns": 1,
    },
]


critic = autogen.AssistantAgent(
    name="Critic",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=utils.llm_config(),
    system_message="You are a critic. You review the work of the writer"
    "and provide constructive feedback to help improve the quality of the content.",
)

WRITER_TASK = """
       Write a concise but engaging blogpost about
       DeepLearning.AI. Make sure the blogpost is
       within 100 words.
       """

writer = autogen.AssistantAgent(
    name="Writer",
    system_message="You are a writer. You write engaging and concise "
    "blogpost (with title) on given topics. You must polish your "
    "writing based on the feedback you receive and give a refined "
    "version. Only return your final work without additional comments.",
    llm_config=utils.llm_config(),
)


critic.register_nested_chats(_review_chats, trigger=writer)

res = critic.initiate_chat(
    recipient=writer, message=WRITER_TASK, max_turns=2, summary_method="last_msg"
)

print(res.summary)
