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
            }
          } else {
            console.warn("Undefined Login Data (subscription fail?)");
          }
        }
      );
      
  }
  //logs out by deleting the login cookie data and redirects back to the beginning
  //should move this to a different component later
  logout(){
    //deletes login cookies
    this.cookieService.delete('user_validated');
    this.cookieService.delete('pass_validated');

    //rediret
    this.router.navigateByUrl('');

  }

}
