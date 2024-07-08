import autogen
import utils

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

reply = writer.generate_reply(messages=[{"content": WRITER_TASK, "role": "user"}])

print(reply)

critic = autogen.AssistantAgent(
    name="Critic",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=utils.llm_config(),
    system_message="You are a critic. You review the work of the writer"
    "and provide constructive feedback to help improve the quality of the content.",
)

#### Start Conversation ####
critic_reply = critic.initiate_chat(
    recipient=writer, message=WRITER_TASK, max_turns=2, summary_method="last_msg"
)

print(critic_reply.summary)
