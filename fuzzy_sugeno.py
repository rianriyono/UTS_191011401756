#Nama   : RIAN RIYONO
#NIM    : 191011401756
#Kelas  : 06TPLE025 

#Fuzzy Sugeno
#Studi Kasus : MESIN CUCI SAMSUNG

#Kecepatan Putaran Mesin : min 5000 rpm dan max 12000 rpm.
#Banyaknya Pakaian  : sedikit 4000 dan banyak 8000.
#Tingkat Kekotoran  : rendah 4000, sedang 5000, dan 6000 tinggi.

def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Pakaian():
    minimum = 4000
    maximum = 8000

    def sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def banyak(self, x):
        if x <= self.minimum:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.minimum, self.maximum)

class Kotor():
    minimum = 4000
    medium = 5000
    maximum = 6000

    def rendah(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def sedang(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def tinggi(self, x):
        if x <= self.medium:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.medium, self.maximum)

class Putaran():
    minimum = 5000
    maximum = 12000
    
    def lambat(self, α):
        if α >= self.maximum:
            return 0
        elif α <= self.minimum:
            return 1

    def cepat(self, α):
        if α <= self.minimum:
            return 0
        elif α >= self.maximum:
            return 1

    # 2 permintaan 3 persediaan
    def inferensi(self, jumlah_pakaian, jumlah_kotor):
        pak = Pakaian()
        ktr = Kotor()
        result = []
        
        # [R1] Jika Pakaian SEDIKIT, dan Kotor RENDAH, 
        #     MAKA Putaran = 500
        α1 = min(pak.sedikit(jumlah_pakaian), ktr.rendah(jumlah_kotor))
        z1 = self.minimum
        result.append((α1, z1))

        # [R2] Jika Pakaian SEDIKIT, dan Kotor SEDANG, 
        #     MAKA Putaran = 10 * jumlah_kotor + 100
        α2 = min(pak.sedikit(jumlah_pakaian), ktr.sedang(jumlah_kotor))
        z2 = 10 * jumlah_kotor + 100
        result.append((α2, z2))

        # [R3] Jika Pakaian SEDIKIT, dan Kotor TINGGI, 
        #     MAKA Putaran = 10 * jumlah_kotor + 200
        α3 = min(pak.sedikit(jumlah_pakaian), ktr.tinggi(jumlah_kotor))
        z3 = 10 * jumlah_kotor + 200
        result.append((α3, z3))

        # [R4] Jika Pakaian BANYAK, dan Kotor RENDAH,
        #     MAKA Putaran = 5 * jumlah_pakaian + 2 * jumlah_kotor
        α4 = min(pak.banyak(jumlah_pakaian), ktr.rendah(jumlah_kotor))
        z4 = 5 * jumlah_pakaian + 2 * jumlah_kotor
        result.append((α4, z4))

        # [R5] Jika Pakaian BANYAK, dan Kotor SEDANG,
        #     MAKA Putaran = 5 * jumlah_pakaian + 4 * jumlah_kotor + 100
        α5 = min(pak.banyak(jumlah_pakaian), ktr.sedang(jumlah_kotor))
        z5 = 5 * jumlah_pakaian + 4 * jumlah_kotor + 100
        result.append((α5, z5))

        # [R6] Jika Pakaian BANYAK, dan Kotor TINGGI,
        #     MAKA Putaran = 5 * jumlah_pakaian + 5 * jumlah_kotor + 300
        α6 = min(pak.banyak(jumlah_pakaian), ktr.tinggi(jumlah_kotor))
        z6 = 5 * jumlah_pakaian + 5 * jumlah_kotor + 300
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_pakaian, jumlah_kotor):
        inferensi_values = self.inferensi(jumlah_pakaian, jumlah_kotor)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])