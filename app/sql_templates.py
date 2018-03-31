create_hardware_table = """CREATE TABLE `hardware` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`sw_id` VARCHAR(10) NULL DEFAULT NULL COLLATE 'utf8_unicode_ci',
	`sw_ip` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8_unicode_ci',
	`portsdown_count` INT(11) NULL DEFAULT '0',
	`first_portdown_time` DATETIME NULL DEFAULT NULL,
	`last_message_send_time` DATETIME NULL DEFAULT NULL,
	`is_notify_enable` TINYINT(1) NULL DEFAULT '1',
	PRIMARY KEY (`id`),
	UNIQUE INDEX `sw_id` (`sw_id`),
	UNIQUE INDEX `sw_ip` (`sw_ip`)
)"""

drop_hardware_table="""DROP TABLE `hardware`"""

select_hw_by_ip="""SELECT sw_id, sw_ip, portsdown_count, first_portdown_time
       FROM hardware
       WHERE sw_ip=%s"""

select_hw_by_id="""SELECT sw_id, sw_ip, portsdown_count, first_portdown_time
       FROM hardware
       WHERE sw_id=%s"""
