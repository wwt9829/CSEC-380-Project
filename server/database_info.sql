USE project;

CREATE TABLE IF NOT EXISTS `users` (
      `user_id` int(11) NOT NULL AUTO_INCREMENT,
      `email` varchar(320) NOT NULL,
      `password` varchar(128) NOT NULL,
      `displayname` varchar(32) NOT NULL,
      `username` varchar(32) NOT NULL,
      `admin` boolean NOT NULL,
      PRIMARY KEY (`user_id`)
    ) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=18 ;

INSERT INTO `users` (`user_id`, `email`, `password`, `displayname`, `username`, `admin`) VALUES
(1, 'test@user.com', 'password', 'test', 'test', 0),
(2, 'admin@user.com', 'password', 'admin', 'admin', 1);
