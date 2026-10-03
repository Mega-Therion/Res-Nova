CREATE TABLE `admin_audit_log` (
	`id` int AUTO_INCREMENT NOT NULL,
	`actorId` int,
	`action` varchar(80) NOT NULL,
	`entityType` varchar(80) NOT NULL,
	`entityId` varchar(160) NOT NULL,
	`summary` text NOT NULL,
	`beforeJson` text,
	`afterJson` text,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `admin_audit_log_id` PRIMARY KEY(`id`)
);
