import java.sql.*;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class UserService {

    public String getUser(String username) throws Exception {
        // ❌ Hardcoded DB credentials
        String url = "jdbc:mysql://localhost:1/appdb";
        String user = "root";
        String password = "password123";

        Connection conn = DriverManager.getConnection(url, user, password);

        // ❌ SQL Injection vulnerability
        String query = "SELECT * FROM users WHERE username = '" + username + "'";
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(query);

        // ❌ Weak encryption (DES)
        String secret = "12345678";
        Cipher cipher = Cipher.getInstance("DES");
        SecretKeySpec key = new SecretKeySpec(secret.getBytes(), "DES");
        cipher.init(Cipher.ENCRYPT_MODE, key);

        return rs.next() ? rs.getString("email") : null;
    }
}