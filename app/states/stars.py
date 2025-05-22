from aiogram.fsm.state import State, StatesGroup


class WithdrawalStarState(StatesGroup):
    enter_amount = State()


class BuyStarState(StatesGroup):
    enter_amount = State()



class BuyStarSelectUserState(StatesGroup):
    enter_username = State()
    smth = State()