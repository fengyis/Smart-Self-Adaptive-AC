Parse.Cloud.define("smartSet",function(request, response){
      var tempObject = Parse.Object.extend("WorkObject");
      var tsetting = 10000;
      var levelNum = 100000; //Low is 1 or 0, Medium is 2, High is 3 or 4 or 5. Shutdown or extreme low is -1.
 
      var interval = 20; //assume 20mins time interval
       
      var query = new Parse.Query(tempObject);
      query.get("mR8AWQdHL3",{
            success: function(tempQuery){
                  var toutdoor = tempQuery.get("Toutdoor");
                  var tindoor = tempQuery.get("Tindoor");
                  var rate = tempQuery.get("FlowRate");
                  var pwork = tempQuery.get("Pwork");
                  var consumption = tempQuery.get("Consumption");
 
                  var updateTime = String(tempQuery.updatedAt);
                  var split = updateTime.split(" ");
                  var week = split[0];
                  var time = split[4];
                  var a = time.split(":");
                  var minute = parseInt(a[0])*60 + parseInt(a[1]);
 
                  if(toutdoor>95){
                        tsetting = 68;
                  }
                  if(toutdoor<=95 && toutdoor>=77){
                        tsetting = 70;
                  }
                  if(toutdoor<77){
                        tsetting = 73;
                  }
 
                  //set working power and fant level
                  temDiff = Math.abs(tsetting-tindoor);
                  if(temDiff>14){
                        levelNum = 3;
                  }
                  if(temDiff>7 && temDiff<=14){
                        levelNum = 2;
                  }
                  if(temDiff>=0 && temDiff<=7){
                        levelNum = 1;
                  }
 
                  if(tindoor<tsetting){
                        levelNum = -1;
                  }
 
                  if(rate>10){
                        levelNum++;
                  }
                  if(rate>20){
                        levelNum++;
                  }
                  if(rate==0){
                        levelNum--;
                  }
 
 
 
                  var temp = new tempObject();
                  var sum = consumption + pwork*interval/(1000*3600);
                  var newConsump = parseFloat(sum.toFixed(2));
                  var totalConsump = parseFloat(sum.toFixed(2));
 
                  temp.set("objectId", "mR8AWQdHL3");
                  temp.save(null,{
                        success: function(temp){
                               
                              if(minute>1440-interval-2 && minute<=1440){                 //At 24:00, reset consumption
                                    newConsump = 0;
                              }
 
                              temp.set("Tsetting", tsetting);
                              var flag = 0;
 
                              if(levelNum == 1 || levelNum == 0){
                                    temp.set("Pwork",2000);
                                    temp.set("Level",20);
                                    temp.set("Consumption", newConsump);
                                    temp.save();
                              }
                              if(levelNum == 2){
                                    flag = 1;
                                    temp.set("Pwork",2500);
                                    temp.set("Level",60);
                                    temp.set("Consumption", newConsump);
                                    temp.save();
                              }
                              if(levelNum == 3 || levelNum == 4 || levelNum == 5){
                                    temp.set("Pwork",3000);
                                    temp.set("Level",90);
                                    temp.set("Consumption", newConsump);
                                    temp.save();
                              }
                              if(levelNum == -1){
                                    temp.set("Pwork",500);
                                    temp.set("Level",5);
                                    temp.set("Consumption", newConsump);
                                    temp.save();
                              }
 
                              response.success("Tsetting is "+tsetting+" LevelNum is "+levelNum+" Consumption is "+newConsump+" flag is "+flag);
                        },
                        error: function(temp){
                            response.error("Got an error "+error.code+" : "+error.message);  
                        }
                  });
                   
                  var flag2 = 0;
                  if(minute>1440-interval-2 && nimute<=1440){             //At 24:00, output whole day power consumption to "Consumption" class
                        flag2 = 1;
                        var setObject = Parse.Object.extend("Consumption");
                        var temp2 = new setObject();
                        temp2.set("objectId","skaj0rt8gN");
                        temp2.save(null, {
                              success: function(temp2){
                                    flag2 = 2;
                                    if(week == "Mon"){
                                          temp2.set("Monday",totalConsump);
                                          temp2.save();
                                    }
                                    if(week == "Tue"){
                                          temp2.set("Tuesday",totalConsump);
                                          temp2.save();
                                    }
                                    if(week == "Wed"){
                                          temp2.set("Wednesday",totalConsump);
                                          temp2.save();
                                    }
                                    if(week == "Thu"){
                                          temp2.set("Thursday",totalConsump);
                                          temp2.save();
                                    }
                                    if(week == "Fri"){
                                          temp2.set("Friday",totalConsump);
                                          temp2.save();
                                    }
                                    if(week == "Sat"){
                                          temp2.set("Saturday",totalConsump);
                                          temp2.save();
                                    }
                                    if(week == "Sun"){
                                          flag2 = 3;
                                          temp2.set("Sunday",totalConsump);
                                          temp2.save();
                                    }
 
                                    //response.success("Tsetting is "+tsetting+" LevelNum is "+levelNum+" totalConsumption is "+totalConsump+" flag2 is "+flag2+" time is "+ time+" minute is "+minute);
 
 
                              },
                              error: function(put, error){
                                    //response.error("Got an error "+error.code+" : "+error.message); 
                              }
 
                        });
 
                  }
 
            }
             
 
      });
});