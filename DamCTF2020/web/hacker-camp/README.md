## web/hacker-camp
>Sponsored challenge provided by HackerOne. Questions/issues go to captainGeech.

>Natasha Drew wants to go to Hacker Camp but doesn't have the grades she needs. Hack into the student portal and change her grades so she can attend.

>hacker-camp.chals.damctf.xyz

* Passing username: admin and password: ' or '1'='1 will log you in as rhonda.daniels. SQL Injection.
* You then get a random cookie encoded in base64, such as ZWE3M2I5ZjVlNWRmNjVjMTlmZjVhMjhkYzg4M2RhZjAyZGM1NjhmYzM2ZGUzYzc3ZDc1NTE1YjdlNDE1Y2ExYzNlYTg0M2Q0ZDgzNjhjZDJkYTIxYTEyOTRiYTFhZThjMDc4MWY5ODViZGZkZTE5NGU2YWNmNzJlMGRiNzFkYjM=. It decrypts as a hex value, such as ea73b9f5e5df65c19ff5a28dc883daf02dc568fc36de3c77d75515b7e415ca1c3ea843d4d8368cd2da21a1294ba1ae8c0781f985bdfde194e6acf72e0db71db3.
* There are some javascript connected with the site:

```javascript=
var staff = {
    admin   :   false,
    name    :   'rhonda.daniels'
}
````

```javascript=
(function(s, objectName) {
    setupLinks = function() {
        if (s.admin) {
            var sl = document.getElementsByClassName("student-link");
            for (i = 0; i < sl.length; i++) {
                let name = sl[i].innerHTML;
                sl[i].style.cursor = 'pointer';
                sl[i].addEventListener("click", function() {
                    window.location = '/update-' + objectName + '/' + this.dataset.id;
                });
            }
        }
    }
    ;
    updateForm = function() {
        var submitButton = document.getElementsByClassName("update-record");
        if (submitButton.length === 1) {
            submitButton[0].addEventListener("click", function() {
                var english = document.getElementById("english");
                english = english.options[english.selectedIndex].value;
                var science = document.getElementById("science");
                science = science.options[science.selectedIndex].value;
                var maths = document.getElementById("maths");
                maths = maths.options[maths.selectedIndex].value;
                var grades = new Set(["A", "B", "C", "D", "E", "F"]);
                if (grades.has(english) && grades.has(science) && grades.has(maths)) {
                    document.getElementById('student-form').submit();
                } else {
                    alert('Grades should only be between A - F');
                }
            });
        }
    }
    ;
    setupLinks();
    updateForm();
}
)(staff, 'student');
````

* The link "/update-" + objectName + "/" + this.dataset.id is interesting.
* On inspecting the students table, each student has a data-id which is their FirstName_LastName in base64. We can base64-encode Natasha_Drew to get TmF0YXNoYV9EcmV3
* We can visit the URL /update-student/TmF0YXNoYV9EcmV3 and change all grades to A to get the flag.

Flag: `dam{n0w_w3_c4n_h4ck_th3_pl4n3t}`