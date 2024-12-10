##Declaration des constantes
OCTETS = 1
BITS = 8 * OCTETS
VERBOSE = 1
VERBOSE_N1 = 42
VERBOSE_N2 = 11
VERBOSE_R1 = 42
VERBOSE_R2 = -11
VERBOSE_BN1 = [0, 1, 0, 0, 1, 1, 0, 0] #76
VERBOSE_BN2 = [0, 0, 1, 0, 1, 0, 1, 0] #42
VERBOSE_BR1 = [1, 0, 1, 1, 0, 1, 0, 0] #-76
VERBOSE_BR2 = [1, 1, 0, 1, 0, 1, 1, 0] #-42
##Fonctions
#1) Conversion de base10 en base2
def DecToBin(base10) :
	"""Convertit un nombre entier naturel en base 10 en base 2
	params :
		base10 : int ; le nombre en base 10
	return :
		response : list ; le nombre converti
	"""
	response = [0] * int(BITS)
	for i in range(len(response)) :
		response[i] = base10 % 2
		base10 //= 2
	response.reverse()
	return response

if VERBOSE :
	#conversion de base10 en base2 avec un nombre entier naturel
	print(f"[*] conversion de {VERBOSE_N1} en binaire : ")
	print(f"[+] Valeur trouvée : {DecToBin(VERBOSE_N1)}")
	print(f"[+] Valeur souhaitee : {bin(VERBOSE_N1)}")
	print()
	#conversion de base10 en base2 avec un nombre entier relatif
	print(f"[*] conversion de {VERBOSE_R2} en binaire : ")
	print(f"[+] Valeur trouvée : {DecToBin(VERBOSE_R2)}")
	print(f"[+] Valeur souhaitee : {bin((2**BITS)+VERBOSE_R2)}")
	print("_" * 50)

#2) Conversion d'entier naturel binaire en base 10
def NaturalBinToDec(base2) :
	"""Convertit un nombre entier naturel base 2 en base 10
	params :
		base2 : int ; le nombre entier naturel en base2
	return :
		response : list ; le nombre converti
	"""
	power = len(base2)-1
	response = 0
	for i in base2 :
		response += int(i) * 2 ** power
		power -= 1
	return response

if VERBOSE :
	print(f"[*] Conversion de {VERBOSE_BN1} (76) en base 10")
	print(f"[+] Valeur trouvee :  {NaturalBinToDec(VERBOSE_BN1)}")
	print(f"[+] Valeur souhaitee : 76")
	print("_" * 50)

#3) Conversion d'entier relatif binaire en base 10
def RelativeBinToDec(base2) :
	"""Convertit un nombre entier relatif en base 2 en base 10
	params :
		base2: int ; le nombre entier relatif en base 2
	return :
		response : list ; le nombre converti
	"""
	power = len(base2)-1
	response = -(abs(base2[0]) * 2 ** power)
	power -= 1
	for i in base2[1:] :
		response += i * 2 ** power
		power -= 1
	return response

if VERBOSE :
	print(f"[*] Conversion de {VERBOSE_BR1} (-76) en base 10")
	print(f"[+] Valeur trouvee :  {RelativeBinToDec(VERBOSE_BR1)}")
	print(f"[+] Valeur souhaitee : -76")
	print("_" * 50)

#3) Addition des nombres entiers naturels binaires
def addBinaryNumbers(bn1,bn2) :
	"""Additioner deux nombres entiers naturels/relatifs binaires
	params :
		bn1 : int ; le premier nombre
		bn2 : int ; le deuxieme nombre
	return :
		response : list ; le resultat
	"""
	cache1 = bn1[:]
	cache2 = bn2[:]
	carry = int()
	response = list()
	cache1.reverse()
	cache2.reverse()

	for i in range(BITS) :
		#s = a xor b xor carry
		#carry = (a or b) and (a or carry) and (b or carry)
		a = cache1[i]
		b = cache2[i]
		s = a^b^carry
		carry = (a or b) and (a or carry) and (b or carry)
		response.append(s)
	response.reverse()
	return response

if VERBOSE :
	print(f"[*] Addition de {VERBOSE_BN1} + {VERBOSE_BN2} = 118")
	print(f"[+] Valeur trouvee : {addBinaryNumbers(VERBOSE_BN1,VERBOSE_BN2)}")
	print(f"[+] Valeur souhaitee : {bin(118)}")
	print()
	print(f"[*] Addition de {VERBOSE_BR1} + {VERBOSE_BR2} = -118")
	print(f"[+] Valeur trouvee : {addBinaryNumbers(VERBOSE_BR1,VERBOSE_BR2)}")
	print(f"[+] Valeur souhaitee : {bin((2**BITS)-118)}")
	print("_" * 50)

#4) oppose
def Oppose(base2) :
	"""Avoir l'opppose d'un nombre binaire
	params :
		base2 : list ; le nombre a convertir
	return :
		response : list ; l'oppose
	"""
	response = list()
	for elem in base2 :
		response.append(int(not elem))
	one = DecToBin(1)
	response = addBinaryNumbers(response,one)
	return response

if VERBOSE :
	print(f"Calcul de l'oppose de {VERBOSE_BN1} (76) = -76")
	print(f"[+] Valeur trouvee : {Oppose(VERBOSE_BN1)}")
	print(f"[+] Valeur souhaitee : {DecToBin(-76)}")
	print()
	print(f"Calcul de l'oppose de {VERBOSE_BR2} (-42) = 42")
	print(f"[+] Valeur trouvee : {Oppose(VERBOSE_BR2)}")
	print(f"[+] Valeur souhaitee : {DecToBin(42)}")
	print("_" * 50)

def subBinaryNumber(b1,b2) :