from aiogram.utils.callback_data import CallbackData


lang_callback = CallbackData("pref_lang", "chosen_lang")

size_callback = CallbackData('size', 'chosen_size')
finish_callback = CallbackData('finished', 'finish')
back_to_menu = CallbackData('button', 'action')

cart_add_cd = CallbackData("cart", "item_id")
cart_delete_cd = CallbackData("cart_delete", "item_id")

quantity_cd = CallbackData("quantity", "action", "amount")

pay_method_cd = CallbackData("payment", "method")

order_phase_cd = CallbackData("phase", "action")
