drop table if exists sanctions.stg_ofac_sdn;
create table sanctions.stg_ofac_sdn (
	ent_num	bigint
	,sdn_name nvarchar(500)
	,sdn_type nvarchar(25)
	,program nvarchar(255)
	,title nvarchar(255)
	,call_sign nvarchar(10)
	,vess_type nvarchar(25)
	,tonnage nvarchar(25)
	,grt nvarchar(10)
	,vess_flag nvarchar(50)
	,vess_owner nvarchar(255)
	,remarks nvarchar(1000)
);