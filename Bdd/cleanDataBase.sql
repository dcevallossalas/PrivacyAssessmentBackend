delete from principles where id > 0;
delete from annotations where id > 0;
delete from cases where id > 0;
delete from laws where id > 0;
delete from normatives where id > 0;

select * FROM principles;
select * from annotations;
select * from cases;
select * from laws;
select * from normatives;