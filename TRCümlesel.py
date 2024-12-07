#!/usr/bin/env python3

import json, sys, subprocess, os, time, threading

class Fonksiyon:
	def __init__(self, args, code):
		self.args = args
		self.code = code
	def run(self, args, vars={}):
		code = self.code
		for n, h in enumerate(self.args):
			code = code.replace(f"!!{h}", str(args[n]))
		result, vars = run(code, vars=vars)
		return result, vars
			
global_vars = {}
lock = threading.Lock()

def run(command, vars={}):
	global global_vars
	if command.startswith("veri "):
		command = command[5:]
		if command.startswith("sayı "): # veri sayı 500
			return int(command[5:]), vars
		elif command.startswith("ondalık "): # veri ondalık 5.500
			return float(command[8:]), vars
		elif command.startswith("metin "): # veri metin Merhaba Dünya!
			return command[6:], vars
		elif command.startswith("liste "): # veri liste veri metin Öğe 1 // veri metin Öğe 2 // veri ondalık 4.5 // veri sayı 827
			command = command[6:]
			ogeler = []
			for h in command.split(" // "):
				if len(h) != 0:
					h, vars = run(h, vars=vars)
					ogeler.append(h)
			return ogeler, vars
		elif command.startswith("demet "): # veri demet veri metin Öğe 1 // veri metin Öğe 2 // veri ondalık 4.5 // veri sayı 827
			command = command[6:]
			ogeler = ()
			for h in command.split(" // "):
				if len(h) != 0:
					h, vars = run(h, vars=vars)
					ogeler = ogeler+(h, )
			return ogeler, vars
		elif command.startswith("kurdistan "): # veri kurdistan
			return None, vars
		elif command.startswith("veritabanı "): # veri veritabanı veri metin Veri İsmi! :: veri sayı 400 /!/ veri metin Yaş? :: veri sayı 3
			command = command[11:]
			ogeler = {}
			for h in command.split(" /!/ "):
				if len(h) != 0:
					h = h.split(" :: ")
					name, vars = run(h[0], vars=vars)
					value, vars = run(h[1], vars=vars)
					ogeler[name] = value
			return ogeler, vars
		elif command.startswith("veritabanı-al "): # veri veritabanı-al veri veritabanı veri metin oge1 :: veri metin hello!;veri metin oge1
			command = command[14:].split(";")
			taban, vars = run(command[0], vars=vars)
			veri, vars = run(command[1], vars=vars)
			return taban[veri], vars
		elif command.startswith("veritabanı-kaydet "): # veri veritabanı-kaydet veri veritabanı veri metin oge1 :: veri metin hello!
			command = command[18:]
			taban, vars = run(command, vars=vars)
			return json.dumps(taban), vars
		elif command.startswith("veritabanı-yükle "): # veri veritabanı-yükle veri metin {"oge1": "hello!"}
			command = command[17:]
			taban, vars = run(command, vars=vars)
			return json.loads(taban)
		elif command.startswith("böl "): # veri böl veri metin , ;veri metin Merhaba, Selam
			command = command[4:]
			bolucu, vars = run(command[:command.find(";")], vars=vars)
			hedef, vars = run(command[command.find(";")+1:], vars=vars)
			if "türk" not in str(hedef).lower() and "turk" not in str(hedef).lower() and "türkiye" not in str(hedef).lower() and "turkiye" not in str(hedef).lower() and "vatan" not in str(hedef).lower():
				return hedef.split(bolucu), vars
			else:
				return ["Vatan Bölünmez!"], vars
		elif command.startswith("birleştir "): # veri birleştir veri metin , ;veri liste veri metin Merhaba // veri metin Selam
			command = command[10:]
			bolucu, vars = run(command[:command.find(";")], vars=vars)
			hedef, vars = run(command[command.find(";")+1:], vars=vars)
			return bolucu.join(hedef), vars
		elif command.startswith("al "): # veri al veri sayı 0;veri metin Hello
			command = command[3:]
			bolge, vars = run(command[:command.find(";")], vars=vars)
			hedef, vars = run(command[command.find(";")+1:], vars=vars)
			return hedef[bolge], vars
		elif command.startswith("aralık al "): # veri aralık al veri sayı 0;veri sayı 2;veri metin Hello
			command = command[10:]
			bolge, vars = run(command[:command.find(";")], vars=vars)
			command = command[command.find(";")+1:]
			bolge2, vars = run(command[:command.find(";")], vars=vars)
			command = command[command.find(";")+1:]
			hedef, vars = run(command[command.find(";")+1:], vars=vars)
			return hedef[bolge:bolge2], vars
		elif command.startswith("getir "): # veri getir veri metin degisken_ismi
			command = command[6:]
			name, vars = run(command, vars=vars)
			return vars[name], vars
		elif command.startswith("ortak-getir "): # veri ortak-getir veri metin global_degisken_ismi
			command = command[12:]
			name, vars = run(command, vars=vars)
			return global_vars[name], vars
		elif command.startswith("hesap topla "): # veri hesap topla veri sayı 10;veri sayı 5
			command = command[12:].split(";")
			value1, vars = run(command[0], vars=vars)
			for h in command[1:]:
				value2, vars = run(h, vars=vars)
				value1 += value2
			return value1, vars
		elif command.startswith("hesap çıkar "): # veri hesap çıkar veri sayı 10;veri sayı 5
			command = command[12:].split(";")
			value1, vars = run(command[0], vars=vars)
			for h in command[1:]:
				value2, vars = run(h, vars=vars)
				value1 -= value2
			return value1, vars
		elif command.startswith("hesap böl "): # veri hesap böl veri sayı 10;veri sayı 2
			command = command[10:].split(';')
			value1, vars = run(command[0], vars=vars)
			for h in command[1:]:
				value2, vars = run(h, vars=vars)
				value1 = value1/value2
			return value1, vars
		elif command.startswith("hesap çarp "): # veri hesap çarp veri sayı 10;veri sayı 5
			command = command[11:].split(';')
			value1, vars = run(command[0], vars=vars)
			for h in command[1:]:
				value2, vars = run(h, vars=vars)
				value1 = value1*value2
			return value1, vars
		elif command.startswith("hesap üst "): # veri hesap üst veri sayı 3;veri sayı 2
			command = command[10:].split(';')
			value1, vars = run(command[0], vars=vars)
			for h in command[1:]:
				value2, vars = run(h, vars=vars)
				value1 = value1**value2
			return value1, vars
		elif command.startswith("hesap mod "): # veri hesap mod veri sayı 10;veri sayı 3
			command = command[10:].split(';')
			value1, vars = run(command[0], vars=vars)
			for h in command[1:]:
				value2, vars = run(h, vars=vars)
				value1 = value1%value2
			return value1, vars
		elif command.startswith("doğru "): # veri doğru 
			return True, vars
		elif command.startswith("yanlış "): # veri yanlış 
			return False, vars
		elif command.startswith("eşittir "): # veri eşittir veri sayı 123;veri sayı 123
			command = command[8:].split(";")
			value1, vars = run(command[0], vars=vars)
			value2, vars = run(command[1], vars=vars)
			return value1 == value2, vars
		elif command.startswith("büyüktür "): # veri büyüktür veri sayı 2;veri sayı 1
			command = command[9:].split(";")
			value1, vars = run(command[0], vars=vars)
			value2, vars = run(command[1], vars=vars)
			return value1 > value2, vars
		elif command.startswith("küçüktür "): # veri küçüktür veri sayı 1;veri sayı 2
			command = command[9:].split(";")
			value1, vars = run(command[0], vars=vars)
			value2, vars = run(command[1], vars=vars)
			return value1 < value2, vars
		elif command.startswith("eşit-büyüktür "): # veri eşit-büyüktür veri sayı 1;veri sayı 1
			command = command[14:].split(";")
			value1, vars = run(command[0], vars=vars)
			value2, vars = run(command[1], vars=vars)
			return value1 >= value2, vars
		elif command.startswith("eşit-küçüktür "): # veri eşit-küçüktür veri sayı 1;veri sayı 1
			command = command[14:].split(";")
			value1, vars = run(command[0], vars=vars)
			value2, vars = run(command[1], vars=vars)
			return value1 <= value2, vars
		elif command.startswith("kod "): # veri kod veri sayı 100
			value, vars = run(command[4:], vars=vars)
			return value, vars
		elif command.startswith("dosya-oku "): # veri dosya-oku veri metin dosya.txt;veri metin utf-8
			command = command[10:].split(";")
			filename, vars = run(command[0], vars=vars)
			try:
				typee, vars = run(command[1], vars=vars)
			except:
				typee = "utf-8"
			with open(filename, "r", encoding=typee) as f:
				return f.read(), vars
		elif command.startswith("dosya-okubit "): # veri dosya-okubit veri metin dosya.txt veri metin utf-32
			command = command[13:].split(";")
			filename, vars = run(command[0], vars=vars)
			try:
				typee, vars = run(command[1], vars=vars)
			except:
				typee = "utf-8"
			with open(filename, "rb") as f:
				return f.read().decode(typee), vars
		elif command.startswith("dosya-yaz "): # veri dosya-yaz veri metin dosya.txt;veri metin utf-8;veri metin Dosya içeriği burada!
			command = command[10:].split(";")
			filename, vars = run(command[0], vars=vars)
			typee, vars = run(command[1], vars=vars)
			command = ";".join(command[2:])
			content, vars = run(command, vars=vars)
			with open(filename, "w", encoding=typee) as f:
				f.write(content)
				return content, vars
		elif command.startswith("dosya-yazbit "): # veri dosya-yazbit veri metin dosya.txt;veri metin utf-8;veri metin Dosya içeriği burada!
			command = command[13:].split(";")
			filename, vars = run(command[0], vars=vars)
			typee, vars = run(command[1], vars=vars)
			command = ";".join(command[2:])
			content, vars = run(command, vars=vars)
			with open(filename, "wb") as f:
				f.write(content.encode(typee))
				return content, vars
		elif command.startswith("mutlak "): # veri mutlak veri ondalık -5.6
			command = command[7:]
			value, vars = run(command, vars=vars)
			return abs(value), vars
		elif command.startswith("uzunluk "): # veri uzunluk veri metin Hello!
			command = command[8:]
			value, vars = run(command, vars=vars)
			return len(value), vars
		elif command.startswith("ascii-kod-değer "): # veri ascii-kod-değer veri metin a
			command = command[16:]
			value, vars = run(command, vars=vars)
			return ord(value), vars
		elif command.startswith("ascii-kod-harf "): # veri ascii-kod-harf veri sayı 97
			command = command[15:]
			value, vars = run(command, vars=vars)
			return chr(value), vars
		elif command.startswith("yuvarlama "): # veri yuvarlama veri ondalık 5.68;veri sayı 1
			command = command[10:].split(";")
			value, vars = run(command[0], vars=vars)
			value2, vars = run(command[1], vars=vars)
			return round(value, value2), vars
		elif command.startswith("minimum "): # veri minimum veri liste veri sayı 5 // veri sayı 10
			command = command[8:]
			value, vars = run(command, vars=vars)
			return min(value), vars
		elif command.startswith("maksimum "): # veri maksimum veri liste veri sayı 5 // veri sayı 10
			command = command[9:]
			value, vars = run(command, vars=vars)
			return max(value), vars
		elif command.startswith("sırala "): # veri sırala veri liste veri sayı 3 // veri sayı 1 // veri sayı 2
			command = command[7:]
			value, vars = run(command, vars=vars)
			return sorted(value), vars
		elif command.startswith("kimlik "): # veri kimlik veri getir veri metin degisken_ismi
			command = command[7:]
			value, vars = run(command, vars=vars)
			return id(value), vars
		elif command.startswith("metinleştir "): # veri metinleştir veri sayı 5
			command = command[12:]
			value, vars = run(command, vars=vars)
			return str(value), vars
		elif command.startswith("sayılaştır "): # veri sayılaştır veri metin 4
			command = command[11:]
			value, vars = run(command, vars=vars)
			return int(value), vars
		elif command.startswith("ondalıklaştır "): # veri ondalıklaştır veri metin 6.77
			command = command[14:]
			value, vars = run(command, vars=vars)
			return float(value), vars
		elif command.startswith("listeleştir "): # veri listeleştir veri metin 12345
			command = command[12:]
			value, vars = run(command, vars=vars)
			return list(value), vars
		elif command.startswith("ters "): # veri ters veri metin 12345
			command = command[5:]
			value, vars = run(command, vars=vars)
			return value[::-1], vars
		elif command.startswith("sistem-argumanlar "): # komut düzenle veri metin degisken_ismi;veri sistem-argumanlar 
			return sys.argv, vars
		elif command.startswith("sistem-sürüm "): # komut düzenle veri metin degisken_ismi;veri sistem-sürüm 
			return "1.0.0 (BASLANGIC) December 2024", vars
		elif command.startswith("sistem-python-sürüm "): # komut düzenle veri metin degisken_ismi;veri sistem-python-sürüm 
			return sys.version, vars
		elif command.startswith("sistem-yol "): # komut düzenle veri metin degisken_ismi;veri sistem-yol 
			return sys.path, vars
		elif command.startswith("sistem-platform "): # komut düzenle veri metin degisken_ismi;veri sistem-platform 
			return sys.platform, vars
		elif command.startswith("sistem-ad "): # komut çıkış yaz veri sistem-ad 
			return os.name, vars
		elif command.startswith("sistem-çalışma-dizini "): # komut çıkış yaz veri sistem-çalışma-dizini
			return os.getcwd(), vars
		elif command.startswith("sistem-dosya-listele "):
			command = command[21:]
			if command != "":
				value, vars = run(command, vars=vars)
				return os.listdir(command), vars
			else:
				return os.listdir(), vars
		elif command.startswith("zaman "):
			return time.time(), vars
		elif command.startswith("python "):
			return eval(command[7:]), vars
		elif command.startswith("fmetin "):
			command = command[7:]
			for v, h in vars.items():
				command = command.replace("!!"+v, str(h))
			for v, h in global_vars.items():
				command = command.replace("!!"+v, str(h))
			return command, vars
		else:
			sys.stderr.write("Hatalı Veri Komutu: "+command[:150]+"...");sys.stderr.flush()
			return None, vars
	elif command.startswith("komut "):
		command = command[6:]
		if command.startswith("düzenle "): # komut düzenle veri metin degisken_ismi;veri sayı 100
			command = command[8:]
			name = command[:command.find(";")]
			name, vars = run(name, vars=vars)
			value = command[command.find(";")+1:]
			value, vars = run(value, vars=vars)
			vars[name] = value
			return name, vars
		elif command.startswith("kaldır "): # komut kaldır veri metin degisken_ismi
			command = command[7:]
			name, vars = run(command, vars=vars)
			del vars[name]
			return name, vars
		if command.startswith("ortak-düzenle "): # komut ortak-düzenle veri metin degisken_ismi;veri sayı 100
			command = command[14:]
			name = command[:command.find(";")]
			name, vars = run(name, vars=vars)
			value = command[command.find(";")+1:]
			value, vars = run(value, vars=vars)
			with lock:
				global_vars[name] = value
			return name, vars
		elif command.startswith("ortak-kaldır "): # komut ortak-kaldır veri metin degisken_ismi
			command = command[13:]
			name, vars = run(command, vars=vars)
			with lock:
				del global_vars[name]
			return name, vars
		elif command.startswith("çıkış yaz "): # komut çıkış yaz veri metin Hello, World!
			command = command[10:]
			value, vars = run(command, vars=vars)
			sys.stdout.write(value)
			return value, vars
		elif command.startswith("çıkış gönder "): # komut çıkış gönder 
			sys.stdout.flush()
			return None, vars
		elif command.startswith("hata yaz "): # komut hata yaz veri metin Hata durumu icin bir yazı
			command = command[9:]
			value, vars = run(command, vars=vars)
			sys.stderr.write(value)
			return value, vars
		elif command.startswith("hata gönder "): # komut hata gönder 
			sys.stderr.flush()
			return None, vars
		elif command.startswith("giriş al "): # komut düzenle veri metin degisken_ismi;komut giriş al 
			out = sys.stdin.read()
			return out, vars
		elif command.startswith("giriş satır-al "): # komut düzenle veri metin degisken_ismi;komut giriş satır-al 
			out = sys.stdin.readline()[:-1]
			return out, vars
		elif command.startswith("fonksiyon "): # komut fonksiyon veri metin degisken_ismi;arguman1 // arguman2;komut çıkış yaz veri metin Merhaba, !!arguman1! Ben deniz !!arguman2.
			command = command[10:]
			name, vars = run(command[:command.find(";")], vars=vars)
			command = command[command.find(";")+1:]
			args = command[:command.find(";")].split(" // ")
			content = command[command.find(";")+1:]
			func = Fonksiyon(args, content)
			vars[name] = func
			return name, vars
		elif command.startswith("fonksiyon-yürüt "): # komut fonksiyon-yürüt veri metin degisken_ismi;veri metin Kullanıcı // veri metin Bilgisayar
			command = command[16:].split(";")
			name, vars = run(command[0], vars=vars)
			command = ";".join(command[1:]).split(" // ")
			args = []
			for h in command:
				value, vars = run(h, vars=vars)
				args.append(value)
			value, vars = vars[name].run(args, vars=vars)
			return value, vars
		elif command.startswith("sistem-çıkış "): # komut sistem-çıkış 
			sys.exit()
			return None, vars
		elif command.startswith("sistem-yürüt "): # komut sistem-yürüt veri liste veri metin mkdir // veri metin ornek_klasor
			command = command[13:]
			cc, vars = run(command, vars=vars)
			output = subprocess.run(cc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			return (output.stdout+output.stderr).decode(), vars
		elif command.startswith("python "): # komut python print("Hello!")
			command = command[7:]
			exec(command)
			return None, vars
		elif command.startswith("eyerki "):
			command = command[7:].split(" > ") # komut eyerki veri eşittir veri doğru ;veri doğru  > komut çıkış yaz veri metin Veriler aynı!
			value, vars = run(command[0], vars=vars)
			command = " > ".join(command[1:])
			if value:
				result, vars = run(command, vars=vars)
				return result, vars
			else:
				return None, vars
		elif command.startswith("eyerki-değilse "): # komut eyerki-değilse veri eşittir veri doğru ;veri yanlış  > komut çıkış yaz veri metin Veriler aynı değil!
			command = command[15:].split(" > ")
			value, vars = run(command[0], vars=vars)
			command = " > ".join(command[1:])
			if not value:
				result, vars = run(command, vars=vars)
				return result, vars
			else:
				return None, vars
		elif command.startswith("hata işleme "): # komut hata işleme veri metin hata_fonksiyonu;veri sayı HatalıSayı
			command = command[12:]
			func = command[:command.find(";")]
			command = command[command.find(";")+1:]
			try:
				return run(command, vars=vars)
			except Exception as e:
				func, vars = run(func, vars=vars)
				return vars[func].run([str(e)], vars=vars)
		elif command.startswith("öğe döngüsü "): # komut öğe döngüsü veri liste veri sayı 1 // veri sayı 2 // veri sayı 3 > komut çıkış yaz veri metinleştir veri hesap üst veri getir veri metin öğe;veri sayı 3
			command = command[12:].split(" > ")
			liste, vars = run(command[0], vars=vars)
			code = " > ".join(command[1:])
			for h in liste:
				vars["öğe"] = h
				value, vars = run(code, vars=vars)
		elif command.startswith("genel döngü "): # komut genel döngü veri doğru  > komut çıkış yaz veri metin Sonsuza kadar metin! 
			command = command[12:].split(" > ")
			olay = command[0]
			code = " > ".join(command[1:])
			while True:
				sonuc, vars = run(olay, vars=vars)
				if not sonuc:
					break
				value, vars = run(code, vars=vars)
		else:
			sys.stderr.write("Hatalı Genel Komut: "+command[:150]+"...");sys.stderr.flush()
			return None, vars
	elif command.startswith("sistem "):
		command = command[7:]
		if command.startswith("yeni ortam "): # sistem yeni ortam komut çıkış yaz veri metin Burası değişkensiz paralel bir ortam!
			command = command[12:]
			return run(command, vars={})
		elif command.startswith("iş parçacığı "): # sistem iş parçacığı komut çıkış yaz veri metin Burası bir yeni iş parçacığı ortamı!
			command = command[13:]
			t = threading.Thread(target=run, args=(command, {}))
			t.start()
		elif command.startswith("yapılandırma "): # sistem yapılandırma /// > !!n > !!r > !!t > !!e > !!tt > !!ct > komut çıkış yaz veri metin Merhaba! Bu TRCümlesel programlama diliyle yapılmış ilk sistemdir.!!nTRCümlesel Nedir? Öğrenmesi ve yapması zor olan türkçe sözdizimi ile yapılmış bir progralama dilidir. Kendi içersinde özelleştirilebilir sözdizimi özellikleri vardır.!!nİsminizi alabilirmiyim?: ///komut düzenle veri metin isim;komut giriş satır-al ///komut çıkış yaz veri fmetin Merhaba !!isim! Sizinle tanışmak çok güzel.!!nProgramı beyendinizmi? (E/H): ///komut düzenle veri metin beyenmek;komut giriş satır-al ///komut eyerki veri eşittir veri getir veri metin beyenmek;veri metin E > komut çıkış yaz veri metin Beğendiğinize çok sevindim...///komut eyerki-değilse veri eşittir veri getir veri metin beyenmek;veri metin E > komut çıkış yaz veri metin Beğenmediğiniz için üzülüyorum :(
			command = command[13:].split(" > ")
			bolucu = command[0]
			yeni_satir = command[1]
			tab = command[2]
			satir_basi = command[3]
			egik_cizgi = command[4]
			tek_tirnak = command[5]
			cift_tirnak = command[6]
			command = " > ".join(command[7:])
			for c in command.split(bolucu):
				c = c.replace(yeni_satir, "\n").replace(satir_basi, "\r").replace(egik_cizgi, "\\").replace(tek_tirnak, "\'").replace(cift_tirnak, "\"")
				result, vars = run(c, vars=vars)
			return None, vars
		elif command.startswith("kod "): # sistem kod /// > komut çıkış yaz veri metin Merhaba, ///komut çıkış yaz veri metin Ben Bilgisayar!
			command = command[4:].split(" > ")
			bolucu = command[0]
			command = " > ".join(command[1:])
			for c in command.split(bolucu):
				result, vars = run(c, vars=vars)
			return None, vars
		else:
			sys.stderr.write("Hatalı Sistem Komutu: "+command[:150]+"...");sys.stderr.flush()
			return None, vars
	else:
		sys.stderr.write("Hatalı Komut Kategorisi: "+command[:150]+"...");sys.stderr.flush()
		return None, vars
import chardet, base64
sys.argv = sys.argv[1:]
import random
class Combiner:
	def __init__(self):
		pass
	def combine(self, target, count):
		target = list(target)
		new = target.copy()
		newtarget = target.copy()
		while len(new) < count:
			newpart = []
			for comb1 in newtarget:
				if len(newpart)+len(new) >= count:
					break
				for comb2 in target:
					newpart.append(comb1+comb2)
					if len(newpart)+len(new) >= count:
						break
			newtarget = newpart.copy()
			new += newpart.copy()
			if len(new) >= count:
				break
		return new[:count]
class ShieldKEY: # Shield Kryptographic Engine for Yield
	def __init__(self, chars="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890@#₺_&-+()/*:;!?<>{}[]"):
		self.main_chars = chars
		self.splitter = chars[0]
		chars = chars[1:]
		self.chars = Combiner().combine(chars, 1114112)
	def encode(self, text):
		new = []
		for h in text:
			i = ord(h)
			new.append(self.chars[i%1114112])
		new = self.splitter.join(new)
		newt = ""
		n = 8264
		for h in new:
			i = (self.main_chars.index(h)-71)+n
			if n%2 == 0:
				n += 293
			else:
				n -= 293
			newt += self.main_chars[i%len(self.main_chars)]
		return newt
	def decode(self, text):
		newt = ""
		n = 8264
		for h in text:
			i = (self.main_chars.index(h)-n)+71
			if n%2 == 0:
				n += 293
			else:
				n -= 293
			newt += self.main_chars[i%len(self.main_chars)]
		text = newt
		new = ""
		for h in text.split(self.splitter):
			new += chr(self.chars.index(h))
		return new
	def convert(self, number, key, gn):
		algo = ((key+gn)**2)%4
		if algo == 0:
			return (number+key)-gn
		elif algo == 1:
			return (number+gn)-key
		elif algo == 2:
			return (number*key)+gn
		else:
			return (number*gn)+key
	def unconvert(self, number, key, gn):
		algo = ((key+gn)**2)%4
		if algo == 0:
			return (number+gn)-key
		elif algo == 1:
			return (number+key)-gn
		elif algo == 3:
			return (number-gn)/key
		else:
			return (number-key)/gn
	def convert_key(self, key):
		newkey = 0
		gn = 1847
		for h in str(key):
			newkey += (ord(h)*1934)-len(str(key))
			if gn%2 == 0:
				gn += ((ord(h)+1847)-len(str(key)))*7200
			else:
				gn -= ((ord(h)-1847)+len(str(key)))*3450
		if newkey%2 == 0:
			newkey = -newkey
		if gn%2 == 0:
			gn = -gn
		return newkey, gn
	def encrypt(self, text, key):
		newkey, gn = self.convert_key(key)
		newtext = ""
		for h in text:
			newtext += chr(self.convert(ord(h), newkey, gn)%1114112)
			if gn%2 == 0:
				gn += len(str(key))*8274
			else:
				gn += len(str(key))*2648
		return newtext
	def decrypt(self, text, key):
		newkey, gn = self.convert_key(key)
		newtext = ""
		for h in text:
			newtext += chr(self.unconvert(ord(h), newkey, gn)%1114112)
			if gn%2 == 0:
				gn += len(str(key))*8274
			else:
				gn += len(str(key))*2648
		return newtext
	def hash(self, text):
		newtext = ""
		n = 826473
		for h in text:
			newtext += chr(self.convert(ord(h), ord(h)*30, ord(h)+283+n)%1114112)
			n += ord(h)
		return newtext
key_engine = None
if len(sys.argv) != 0:
	filename = sys.argv[0]
	with open(filename, 'rb') as f:
		raw_data = f.read()
		enkod = chardet.detect(raw_data[128:])["encoding"]
		if enkod == None:
			enkod = "utf-8"
	i = raw_data.decode(enkod)
	if "trcc" in sys.argv:
		key_engine = ShieldKEY(chars="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890")
		newi = key_engine.encode(key_engine.encrypt(i, "TRCC"*8))
		if not filename.endswith(".trcc"):
			filename = ".".join(filename.split(".")[:-1])+".trcc"
		with open(filename, "w") as f:
			f.write(newi)
	else:
		if filename.endswith(".trcc"):
			key_engine = ShieldKEY(chars="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890")
			i = key_engine.decrypt(key_engine.decode(i), "TRCC"*8)
		run(i, vars={})
else:
	print("TRCümlesel v1.0.0 - Manuel Derleme Modu")
	print()
	vars = {}
	while True:
		i = input(">>> ")
		result, vars = run(i, vars=vars)