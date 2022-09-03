insert into account (email, password) values ('kellcock0@trellian.com', '3MB1Ysuh');
insert into account (email, password) values ('eburchett1@mozilla.com', 'VoLTKCnT');
insert into account (email, password) values ('kmathieu2@miibeian.gov.cn', 'WjQDYc6lbDZ6');
insert into account (email, password) values ('aoven3@163.com', 'YHyh4o6kahs');
insert into account (email, password) values ('kblankau4@indiegogo.com', 'GRQbGTAo1v9');
insert into account (email, password) values ('asandyfirth5@livejournal.com', 'PrTkgVN2DM1G');
insert into account (email, password) values ('fshirer6@state.tx.us', 'bTWqfAuJI9');
insert into account (email, password) values ('kshalloo7@usda.gov', 'lyHFRStq');
insert into account (email, password) values ('maustins8@wikimedia.org', 'HSbTpqn');
insert into account (email, password) values ('vmacilraith9@rediff.com', 'VbhXpbJpLUQ');

insert into book (isbn, title, author) values ('718229515-6', 'Riverworld', 'Danie Osmond');
insert into book (isbn, title, author) values ('994203207-X', 'NATO''s Secret Armies (Gladio: L''esercito segreto della Nato)', 'Shellie Snazle');
insert into book (isbn, title, author) values ('597971252-6', 'Pretty/Handsome', 'Evyn Thirlwell');
insert into book (isbn, title, author) values ('081175910-5', 'Lake City', 'Wolf Nyssen');
insert into book (isbn, title, author) values ('276030421-3', 'Calendar Girl', 'Hermann Shegog');
insert into book (isbn, title, author) values ('066093023-4', 'Sam Peckinpah''s West: Legacy of a Hollywood Renegade', 'Lionel Cansdall');
insert into book (isbn, title, author) values ('166106603-8', 'Charlie''s Country', 'Henrie Heinzler');
insert into book (isbn, title, author) values ('032728936-8', 'Goldene Zeiten', 'Cortney Wennam');
insert into book (isbn, title, author) values ('693974864-4', 'Kummelin jackpot', 'Rafaelia Bollini');
insert into book (isbn, title, author) values ('823819572-1', 'You Can Count on Me', 'Reube Heyns');

delete from borrow;
insert into borrow (isbn, email) (select isbn, email from account, book where random() < 0.1);