[README.md](https://github.com/user-attachments/files/35203298/README.md)
# DNS Sinkhole

This Python project demonstrates how a DNS blocklist changes the IPv4 address returned for a selected domain. The server and client run on the same computer. The demo works offline and requires Python 3. Use `dig` on macOS or `nslookup` on Windows.

## Run the demo on macOS

1. On GitHub, select **Code → Download ZIP**. Extract the archive and open the folder containing `sinkhole.py` in VS Code.
2. Open the local `blocklist.txt`, remove `ads.test` if present, and save. This gives the demonstration a baseline.
3. Select **Terminal → New Terminal** and run the server from the project folder:

   ```bash
   python3 sinkhole.py
   ```

   When `Listening on 127.0.0.1 port 5300` appears, leave this terminal open.

4. Open a **second terminal** and query the local server:

   ```bash
   dig @127.0.0.1 -p 5300 ads.test A +short
   ```

   Expected reply: `192.0.2.20`.

5. Add `ads.test` on its own line in `blocklist.txt` and save. Repeat the command from step 4. The reply changes to `0.0.0.0`. The server reads the blocklist on each query, so the new rule takes effect immediately.

6. In the second terminal, query the control domain:

   ```bash
   dig @127.0.0.1 -p 5300 college.test A +short
   ```

   Expected reply: `192.0.2.10`. This shows that the rule applies only to the listed domain.

To reverse the rule, remove `ads.test`, save, and repeat step 4. The reply returns to `192.0.2.20`. To stop the server, press **Control+C** in the first terminal.

## Run the demo on Windows 10 or 11

1. Install Python 3 if needed. Download the repository using **Code → Download ZIP**, right-click the ZIP, select **Extract All**, and open the extracted folder containing `sinkhole.py` in VS Code.
2. Open `blocklist.txt`, remove `ads.test` if present, and press **Ctrl+S**.
3. Select **Terminal → New Terminal**. In the PowerShell terminal, start the server:

   ```powershell
   py -3 sinkhole.py
   ```

   If Windows does not recognize `py`, use `python sinkhole.py` with Python 3 installed. Leave this terminal running when it shows `Listening on 127.0.0.1 port 5300`.
4. Open a **second PowerShell terminal** and query the server:

   ```powershell
   nslookup -port=5300 -type=A ads.test. 127.0.0.1
   ```

   Read the **Address** below **Name: ads.test**. It should be `192.0.2.20`. The address `127.0.0.1` near the top identifies the DNS server itself.
5. Add `ads.test` on its own line in `blocklist.txt`, press **Ctrl+S**, and repeat step 4. The answer should now be `0.0.0.0`.
6. Check the control domain:

   ```powershell
   nslookup -port=5300 -type=A college.test. 127.0.0.1
   ```

   Its address should still be `192.0.2.10`. To reset the demo, remove `ads.test` from the blocklist and save. Press **Ctrl+C** in the first terminal to stop the server.
