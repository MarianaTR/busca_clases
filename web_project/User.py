class User():

  def __init__(self, id: int,  name: str, email: str, password: str,
          phone: str, univerdidad: str, cargo: str, direcc: str):
    self.id = id
    self.name = name
    self.email = email
    self.password = password
    self.phone = phone
    self.univerdidad = univerdidad
    self.cargo = cargo
    self.direcc = direcc

  def to_JSON(self):
    return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'password': self.password,
        'phone': self.phone,
        'univerdidad': self.univerdidad,
        'cargo': self.cargo,
        'direcc': self.direcc
    }
