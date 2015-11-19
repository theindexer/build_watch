Use jenkins.conf to configure

------------------------------
{
  "servers": {
    "someId" : "http://jenkins1.mydomain.startup",
    "anotherId" : "http://jenkins2.mydomain.startup"
  },
  "jobs": {
    "myBuild", "someId",
    "myOtherBuild", "someId",
    "lonelyBuild", "anotherId"
  }
}