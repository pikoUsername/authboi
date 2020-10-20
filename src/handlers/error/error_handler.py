from src.utils.misc.logging import logging

from src.loader import dp

# handler by Latend and yes i just copyed that code, beacuse why not(
@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """
    from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                          CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                          MessageTextIsEmpty, RetryAfter,
                                          CantParseEntities, MessageCantBeDeleted)

    if isinstance(exception, CantDemoteChatCreator):
        logging.debug("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logging.debug('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        logging.debug('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.debug('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.debug('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logging.info(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
    logging.exception(f'Update: {update} \n{exception}')

"""
@dp.error_handler()
class Erorrorhanler:
    def __init__(self, update, exception):
        self.update = update
        self.exception = exception
        
    def check(self):
        # and yes its against that
            from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                          CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                          MessageTextIsEmpty, RetryAfter,
                                          CantParseEntities, MessageCantBeDeleted)

		if isinstance(exception, CantDemoteChatCreator):
	        logging.debug("Can't demote chat creator")
	        return True

	    if isinstance(exception, MessageNotModified):
	        logging.debug('Message is not modified')
	        return True
	    if isinstance(exception, MessageCantBeDeleted):
	        logging.debug('Message cant be deleted')
	        return True

	    if isinstance(exception, MessageToDeleteNotFound):
	        logging.debug('Message to delete not found')
	        return True

	    if isinstance(exception, MessageTextIsEmpty):
	        logging.debug('MessageTextIsEmpty')
	        return True

	    if isinstance(exception, Unauthorized):
	        logging.info(f'Unauthorized: {exception}')
	        return True

	    if isinstance(exception, InvalidQueryID):
	        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
	        return True

	    if isinstance(exception, TelegramAPIError):
	        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
	        return True
	    if isinstance(exception, RetryAfter):
	        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
	        return True
	    if isinstance(exception, CantParseEntities):
	        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
	        return True
	    logging.exception(f'Update: {update} \n{exception}')
"""
