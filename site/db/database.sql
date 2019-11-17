USE chaimtube;

CREATE TABLE IF NOT EXISTS `Account` (
      `user_id` int(11) NOT NULL AUTO_INCREMENT,
      `Username` varchar(32) NOT NULL,
      `DisplayName` varchar(32) NOT NULL,
      `PasswordHash` varchar(256) NOT NULL,
      PRIMARY KEY (`user_id`)
    );

INSERT INTO `Account` (`user_id`, `Username`, `DisplayName`, `PasswordHash`) VALUES
(1, 'test@user.com', 'Test Test', 'password'),
(2, 'admin@user.com', 'Admin Admin', 'password');