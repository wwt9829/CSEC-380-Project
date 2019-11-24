USE chaimtube;

CREATE TABLE IF NOT EXISTS `Account` (
      `user_id` int(11) NOT NULL AUTO_INCREMENT,
      `Username` varchar(32) NOT NULL,
      `DisplayName` varchar(32) NOT NULL,
      `Salt` varchar(16) NOT NULL,
      `PasswordHash` varchar(256) NOT NULL,
      PRIMARY KEY (`user_id`)
    );

CREATE TABLE IF NOT EXISTS `Video` (
      `video_id` int(11) NOT NULL AUTO_INCREMENT,
      `user_id` int(11) NOT NULL,
      `Username` varchar(32) NOT NULL,
      `FileName` varchar(32) NOT NULL,
      PRIMARY KEY (`video_id`),
      CONSTRAINT `fk_video_account`
          FOREIGN KEY (user_id) REFERENCES Account (user_id)
          ON DELETE CASCADE
          ON UPDATE RESTRICT
    ) ENGINE = InnoDB;

INSERT INTO `Account` (`user_id`, `Username`, `DisplayName`, `Salt`, `PasswordHash`) VALUES
(1, 'test@user.com', 'Test Test', '38DcRn49QeTx8aJl', '7b063fc3b1fe75458cef876595524681fbaacb4160076ffe29e46b8813313936'),
(2, 'admin@user.com', 'Admin Admin', 'GZDxKjvdZUA5u4tP', '7476de220a716fec6159e5f9129b4caf80e052c850531cf3291b9abefd831400');
