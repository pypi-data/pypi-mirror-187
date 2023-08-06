from galaxybrain.rules import Rule
from galaxybrain.workflows import Workflow, CompletionStep
from galaxybrain.prompts import Prompt
from tests.mocks.mock_driver import MockCompletionDriver


class TestWorkflow:
    def test_constructor(self):
        rule = Rule("test")
        driver = MockCompletionDriver()
        workflow = Workflow(completion_driver=driver, rules=[rule])

        assert workflow.completion_driver is driver
        assert workflow.root_step is None
        assert workflow.rules[0].value is "test"
        assert workflow.memory is not None

    def test_steps_order(self):
        first_step = CompletionStep(input=Prompt("test1"))
        second_step = CompletionStep(input=Prompt("test2"))
        third_step = CompletionStep(input=Prompt("test3"))

        workflow = Workflow(
            completion_driver=MockCompletionDriver(),
            root_step=first_step
        )

        workflow.add_step(second_step)
        workflow.add_step(third_step)

        assert workflow.steps()[0] is first_step
        assert workflow.steps()[1] is second_step
        assert workflow.steps()[2] is third_step
        assert workflow.last_step() is third_step

    def test_add_step(self):
        step = CompletionStep(input=Prompt("test1"))
        workflow = Workflow(completion_driver=MockCompletionDriver())

        workflow.add_step(step)

        assert step in workflow.steps()

    def test_add_steps(self):
        step1 = CompletionStep(input=Prompt("test1"))
        step2 = CompletionStep(input=Prompt("test2"))
        workflow = Workflow(completion_driver=MockCompletionDriver())

        workflow.add_steps(step1, step2)

        assert step1 in workflow.steps()
        assert step2 in workflow.steps()

    def test_to_prompt_string(self):
        workflow = Workflow(
            completion_driver=MockCompletionDriver(),
            root_step=CompletionStep(input=Prompt("to_string"))
        )

        workflow.start()

        assert "ack" in workflow.to_prompt_string()
        assert "to_string" in workflow.to_prompt_string()
