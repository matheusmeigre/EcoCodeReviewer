// TESTE 2: JavaScript - Boolean Redundancy
// Expectativa: Deve detectar comparação redundante e sugerir return direto

function isActive(user) {
  if (user.active == true) return true;
  else return false;
}

function isAdmin(user) {
  if (user.role == "admin") {
    if (user.enabled == true) return true;
    else return false;
  }
  return false;
}
