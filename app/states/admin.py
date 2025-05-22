from aiogram.fsm.state import State, StatesGroup


class EditStarCostState(StatesGroup):
    amount = State()


class AddStarCostState(StatesGroup):
    amount = State()


class EditTextState(StatesGroup):
    text = State()


class SendAllState(StatesGroup):
    text = State()
