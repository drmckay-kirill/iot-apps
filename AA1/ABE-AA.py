from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
from Crypto import Random
from Crypto.Cipher import AES
from charm.core.engine.util import objectToBytes, bytesToObject
import hashlib, base64

class ABEAttributeAuthority:
    """ Simple Attribute Authority Cryptography with AND-Gates without any features """
    def __init__(self):
        self.bs = 32
        self.group = PairingGroup('SS512')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def Setup(self):
        """ Setup ABE cryptosystem 
        return MasterKey and PublicKey objects """

        g, w = self.group.random(G1), self.group.random()
        Y = pair(g, g) ** w

        a_private, a_private_lids, a_private_star = [], [], []
        A_public, A_public_lids, A_public_star = [], [], []

        for i in range(len(self.attributes)):
            a_private.append(self.group.random())
            a_private_lids.append(self.group.random())
            a_private_star.append(self.group.random())
            A_public.append(g ** a_private[i])
            A_public_lids.append(g ** a_private_lids[i])
            A_public_star.append(g ** a_private_star[i])

        PK = {'g': g, 'Y': Y, 'A': A_public, 'A_lids': A_public_lids, 'A_star': A_public_star}
        MK = {'w': w, 'a': a_private, 'a_lids': a_private_lids, 'a_star': a_private_star}
        return (MK, PK)
    
    def SetAttributesList(self, attr):
        """ Set list of string attributes """
        self.attributes = attr

    def GetAttributesMask(self, DeviceAttributes):
        """ Return int array for and-gate attribute, 0 - not used, 1 - used """
        res = []
        for attribute in self.attributes:
            if attribute in DeviceAttributes:
                res.append(1)
            else:
                res.append(0)
        return res

    def GenerateSecretKey(self, MK, PK, DeviceAttributes):
        """ DeviceAttributes - attributes list
        Return secret key object """
        L = self.GetAttributesMask(DeviceAttributes)
        D, s = [], 0

        for i in range(len(L)):
            si = self.group.random()
            s += si
            di = []
            if L[i] == 1:
                di.append(PK['g'] ** (si / MK['a'][i]))
            elif L[i] == 0:
                di.append(PK['g'] ** (si / MK['a_lids'][i]))
            else:
                raise "Invalid attribute mark!"
            di.append(PK['g'] ** (si / MK['a_star'][i]))
            D.append(di)

        D_zero = PK['g'] ** (MK['w'] - s)
        SK = {'D_zero': D_zero, 'D': D}
        return SK
        
    def Encrypt(self, PK, M, DeviceAttributes):
        """ Encrypts message M (from Gt) under ciphertext policy W (array) """
        W = self.GetAttributesMask(DeviceAttributes)
        r = self.group.random()
        C_wave = (PK['Y'] ** r) * M
        C_zero = PK['g'] ** r
        C = []
        for i in range(len(W)):
            if W[i] == 1:
                C.append(PK['A'][i] ** r)
            elif W[i] == 0:
                C.append(PK['A_lids'][i] ** r)
            elif W[i] == -1:
                C.append(PK['A_star'][i] ** r)
            else:
                raise "Incorrect attribute mask!"
        CT = {'C_zero': C_zero, 'C_wave': C_wave, 'C': C, 'W': W}
        return CT

    def Decrypt(self, SK, CT):
        """ Decrypts cyphertext by using secret key associated with the attribute list  """
        if len(CT['W']) != len(SK['D']):
            raise "Incorrect length of cipher text!"
        z = 1
        for i in range(len(CT['W'])):
            if CT['W'][i] == -1:
                val = pair(CT['C'][i], SK['D'][i][1])
            elif CT['W'][i] == 0 or CT['W'][i] == 1:
                val = pair(CT['C'][i], SK['D'][i][0])
            else:
                raise "Incorrect ciphertext attributes!"
            z *= val

        res = CT['C_wave'] / (pair(CT['C_zero'], SK['D_zero']) * z)
        return res

    def EncryptHybrid(self, PK, message, DeviceAttributes):
        """ Encrypts text under ciphertext policy W """
        M = self.group.random(GT)
        key = hashlib.sha256(objectToBytes(M, self.group)).digest()
        raw = self._pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        EncryptedMessage = base64.b64encode(iv + cipher.encrypt(raw))
        CT = self.Encrypt(PK, M, DeviceAttributes)
        return (CT, EncryptedMessage)      

    def DecryptHybrid(self, EncryptedMessage, SK, CT):
        M = self.Decrypt(SK, CT)
        key = hashlib.sha256(objectToBytes(M, self.group)).digest()
        enc = base64.b64decode(EncryptedMessage)
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        DecryptedMessage = self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        return DecryptedMessage

def main():
    print('ABE scheme for AA TEST')
    Message = 'SCIENCE!!!'
    print('Plain text: ' + Message)

    center = ABEAttributeAuthority()
    center.SetAttributesList(["Teapot", "Lamp", "Door", "Microwave", "WaterTap", "Washer", "Ventilator"])
    MK, PK = center.Setup()
    SK = center.GenerateSecretKey(MK, PK, ["Teapot"])   
    
    text = 'SCIENCE!!!'
    CT, EncryptedMessage = center.EncryptHybrid(PK, text, ["Teapot"])
    assert center.DecryptHybrid(EncryptedMessage, SK, CT) == text, "Failed decryption!"
    CT, EncryptedMessage = center.EncryptHybrid(PK, text, ["Teapot", "Lamp"])    
    assert center.DecryptHybrid(EncryptedMessage, SK, CT) != text, "Failed decryption!"

if __name__ == "__main__":
    main()   
