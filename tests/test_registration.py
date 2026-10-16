import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users
from registration import registration as reg

@pytest.fixture(scope="module")
def setup_database():
    """Testlerden önce veri tabanını oluşturmak ve testlerden sonra temizlemek için kullanılan test düzeneği."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Test sırasında veri tabanı bağlantısı oluşturur ve testten sonra bağlantıyı kapatır."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Veri tabanı ve 'users' tablosunun oluşturulmasını test eder."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "'users' tablosu veri tabanında bulunmalıdır."

def test_add_new_user(setup_database, connection):
    """Yeni bir kullanıcının eklenmesini test eder."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Kullanıcı veri tabanına eklenmiş olmalıdır."

# İşte yazabileceğiniz bazı testler:
"""
Var olan bir kullanıcı adıyla kullanıcı eklemeye çalışmayı test etme.
Başarılı kullanıcı doğrulamasını test etme.
Var olmayan bir kullanıcıyla doğrulama yapmayı test etme.
Yanlış şifreyle doğrulama yapmayı test etme.
Kullanıcı listesinin doğru şekilde görüntülenmesini test etme.
"""


def test_ayni_kullanici(tmp_path, monkeypatch):
    monkeypatch.setattr(reg, "DB_NAME", str(tmp_path / "test.db"))
    reg.create_db()

    ilk = reg.add_user("ali", "ali@example.com", "1234")
    ikinci = reg.add_user("ali", "ali@example.com", "1234")

    assert ilk is True
    assert ikinci is False


def test_basarili_giris(tmp_path, monkeypatch):
    monkeypatch.setattr(reg, "DB_NAME", str(tmp_path / "giris.db"))
    reg.create_db()

    reg.add_user("deneme", "deneme@mail.com", "1234")

    sonuc = reg.authenticate_user("deneme", "1234")

    assert sonuc is True

def test_kullanici_listesi(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(reg, "DB_NAME", str(tmp_path / "liste.db"))
    reg.create_db()

    reg.add_user("zeynep", "zeynep@mail.com", "1234")
    reg.display_users()

    sonuc = capsys.readouterr().out

    assert "zeynep" in sonuc


###def test_ayni_kullanici(setup_database):
 ###   ilk = add_user("Ali Süper Ultra Adam", "ali@ekmail.com", "aliaslindasüpheliai123")
 ###   ikinci = add_user("Ali Süper Ultra Adam", "ali@ekmail.com", "aliaslindasüpheliai123")

###    assert ilk is True
###    assert ikinci is False

### ALİ SÜPER ADAMLARINDA KODLARDA YAZILMA HAKKI VARDIR ONLARINDA HAKLARI VARDIR BİZİ DUYUN PYTHON BİZİ DUY PYTHON