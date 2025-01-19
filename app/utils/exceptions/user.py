class UserEmailNotFoundError(Exception):
	"""Raised when the user email is not found in the database"""
	def __init__(self, email: str) -> None:
		self.email = email
		self.message = f'User with email {email} not found'
		super().__init__(self.message)


class UserIdNotFoundError(Exception):
	"""Raised when the user id is not found in the database"""
	def __init__(self, user_id: int) -> None:
		self.user_id = user_id
		self.message = f'User with id {user_id} not found'
		super().__init__(self.message)
