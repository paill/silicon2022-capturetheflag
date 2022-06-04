DROP TABLE IF EXISTS command;
DROP TABLE IF EXISTS beacon;

CREATE TABLE command (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cmd TEXT NOT NULL,
  result TEXT
);

CREATE TABLE beacon (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  status TEXT
);

INSERT INTO command (cmd, result)
VALUES
("exec 2 echo $FLAG", "SILICON{00p5_k00P45_13fT_tH31r_C2_rUNn1Ng}"),
("exec 2 whoami", "luigi"),
("exec 2 download princess-toadstool.tar.gz", "successfully downloaded princess-toadstool.tar.gz from target"),
("exec 2 upload .hellofriend.txt", "uploaded .hellofriend.txt to target");

INSERT INTO beacon (name, status)
VALUES
("local-test-beacon", "running - last reply 3 seconds ago"),
("mario-bros-plumbing", "disconnected"),
("SILICON{535510n_C00k135_5h0u1d_b3_pR0p3r1y_h4ND13d}", NULL)
