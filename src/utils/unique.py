
import  secrets
import  string


class Unique():
  @staticmethod
  def id(*, length = 10):
    alpha = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alpha) for _ in range(length))

