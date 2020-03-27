import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';
import { GraphService } from '../graph.service';
import { strictEqual } from 'assert';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit {
  graphData;

  constructor(
    private user : UserService,
    private cookieService : CookieService,
    private router : Router,
    private graphService : GraphService
  ) { 
  }

  ngOnInit() {
    //set the component's graphData. valid if already logged in
    //
    let cookieData = {'user_validated': this.cookieService.get('user_validated'), 'pass_validated' : this.cookieService.get('pass_validated')};
    
    this.user.getGraphData(cookieData)
      .subscribe(
        (result) => {
          this.graphService.graphData = result; //set the graph component's graphData to the result of this call
        }
      )
      .add(
        () => {
          if (this.graphService.graphData != undefined){
            if (this.graphService.graphData.success == true){

              //GRAPH
              console.log("Valid Login Data. Graph Data Retrieved")

              //any listdata that would be useful to save now
              for (let v of this.graphService.graphData['graph']['vertices']){
                //add a array for vertex neighbors for easy access
                v['neighbors'] = new Array();
                for (let n of this.graphService.GetNeighbors(this.graphService.graphData['graph'], v)){
                  v['neighbors'].push(this.graphService.FindVertex(this.graphService.graphData['graph']['vertices'],n));
                };
              }

              //update graph form values to default values
              for (let c of this.graphService.graphData['graph']['classifications']){
                let string = "settings_editClassification_" + c.id.toString(10);
                console.log(string);

              }

              this.graphData = this.graphService.graphData;

            } else {
              console.warn("Invalid Login Data.");
              //redirect
              this.router.navigateByUrl('');
            }
          } else {
            console.warn("Undefined Login Data (subscription fail?)");
          }
        }
      );
      
  }
  
  //updates the database with the current graphData
  updateDatabase(){
    let updateResponse;
    //reset the "neighbors" value
    for (let v of this.graphService.graphData['graph']['vertices']){
      v['neighbors'] = undefined;
    }

    this.user.updateGraphData(this.graphService.graphData)
      .subscribe(
        (result) => {
          updateResponse = result;
        }
      ).add(
        () => {
          if (updateResponse != undefined){
            if (updateResponse.success == true){
              console.log('Database was successfully updated with the client\'s current graphData');
            } else {
              console.log('UpdateResponse returned failure');
            }
          } else {
            console.log('UpdateResponse returned undefined');
          }
        }
      );
  }

  //logs out by deleting the login cookie data and redirects back to the beginning
  //should move this to a different component later
  logout(){
    //update db
    this.updateDatabase();

    //deletes login cookies
    this.cookieService.delete('user_validated');
    this.cookieService.delete('pass_validated');

    //redirect
    this.router.navigateByUrl('');
  }

  //simple display scripts
  toggleDisplay(elementID){
    let settings = document.getElementById(elementID);
    if (settings.style.display == "block") {
        settings.style.display = "none";
    } else {
        settings.style.display = "block";
    }
  }

}
