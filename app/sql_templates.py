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

drop_hardware_table=""" DROP TABLE `hardware` """

select_hw_by_ip=""" SELECT sw_id, sw_ip, portsdown_count, first_portdown_time
       FROM hardware
       WHERE sw_ip=%s
       """

select_hw_by_id=""" SELECT sw_id, sw_ip, portsdown_count, first_portdown_time
       FROM hardware
       WHERE sw_id=%s
       """

insert_new_hw=""" INSERT INTO hardware (sw_id,sw_ip,portsdown_count,first_portdown_time)
        VALUES (%s,%s,%s,%s)
        """

update_by_ip=""" UPDATE `hardware` SET `portsdown_count`=%s, `first_portdown_time`=%s WHERE  `sw_ip`=%s """
update_by_id=""" UPDATE `hardware` SET `portsdown_count`=%s, `first_portdown_time`=%s WHERE  `sw_id`=%s """

#insert value
#nowTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
# args = ("12", None, 1, nowTime)
# result = db_worker._testQuery(sql_templates.insert_new_hw,args)
