import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';

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
  ) { 
    //this.graphData = this.user.graphData;
  }

  ngOnInit() {
    //set the component's graphData. valid if already logged in
    //

    let cookieData = {'user_validated': this.cookieService.get('user_validated'), 'pass_validated' : this.cookieService.get('pass_validated')};
    
    this.user.getGraphData(cookieData)
      .subscribe(
        (result) => {
          this.graphData = result; //set the graph component's graphData to the result of this call
        }
      )
      .add(
        () => {
          if (this.graphData != undefined){
            if (this.graphData.success == true){

              //GRAPH
              console.log("Valid Login Data. Graph Data Retrieved")

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
    this.user.updateGraphData(this.graphData)
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

  //the following are simple actions to modify the graph
  AddVertex(n){
    let vertices = this.graphData['graph']['vertices'];
  }
  DeleteVertex(n){

  }
  EditVertex(n){

  }

  AddEdge(e){
    let edges = this.graphData['graph']['edges'];

  }
  DeleteEdge(e){

  }
  EditEdge(e){

  }

  AddClassification(c){
    let classifications = this.graphData['graph']['classifications'];
    
  }
  DeleteClassification(c){

  }
  EditClassification(c){

  }

}
