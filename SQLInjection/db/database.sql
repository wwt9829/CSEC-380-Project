USE chaimtube;

CREATE TABLE IF NOT EXISTS `Account` (
      `user_id` int(11) NOT NULL AUTO_INCREMENT,
      `Username` varchar(32) NOT NULL,
      `DisplayName` varchar(32) NOT NULL,
      `PasswordHash` varchar(256) NOT NULL,
      PRIMARY KEY (`user_id`)
    );

CREATE TABLE IF NOT EXISTS `Video` (
      `video_id` int(11) NOT NULL AUTO_INCREMENT,
      `user_id` int(11) NOT NULL,
      `FileName` varchar(32) NOT NULL,
      `VideoURL` varchar(256) NOT NULL,
      PRIMARY KEY (`video_id`)
    );

INSERT INTO `Account` (`user_id`, `Username`, `DisplayName`, `PasswordHash`) VALUES
(1, 'test@user.com', 'Test Test', '7b063fc3b1fe75458cef876595524681fbaacb4160076ffe29e46b8813313936'),
(2, 'admin@user.com', 'Admin Admin', '7476de220a716fec6159e5f9129b4caf80e052c850531cf3291b9abefd831400');