import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';


@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit {
  graphData;

  constructor(
    private user : UserService,
  ) { 
    //this.graphData = this.user.graphData;
  }

  ngOnInit() {
    //set the component's graphData. valid if already logged in
    //
    this.user.accessSession()
      .subscribe(
        (result) => {
          this.graphData = result; //set the graph component's graphData to the result of this call
        }
      )
      .add(
        () => {
          if (this.graphData != undefined){
            if (this.graphData.success == true){
              console.log("Valid Graph Data. User is logged in.")
            } else {
              console.warn("Invalid Graph Data. (not logged in or bad credentials)");
            }
          } else {
            console.warn("Undefined Graph Data (subscription fail?)");
          }
        }
      );
  }

}
