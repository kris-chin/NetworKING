import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';
import { GraphService } from '../graph.service';
import { FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit {
  graphData;
  vertexForm; classForm; edgeForm; //used in modifying the graphData

  constructor(
    private user : UserService,
    private cookieService : CookieService,
    private router : Router,
    private graphService : GraphService,
    private formBuilder : FormBuilder,
  ) { 
    this.vertexForm = formBuilder.group({ //used in modifying the graphData
      id : null,
      name : null,
      type : null,
      type_id : null,
      health : null,
      shape : null,
      notes : null
    });
    this.classForm = formBuilder.group({ //used in modifying the graphData
      id : null,
      name : null,
      color : null,
      count : null
    });
    this.edgeForm = formBuilder.group({ //used in modifying the graphData
      id : null,
      name : null,
      vertex1 : null,
      vertex1_id : null,
      vertex2 : null,
      vertex2_id : null,
      color : null,
      size : null,
      style : null
    });
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

              //any listdata that would be useful to save now
              for (let v of this.graphData['graph']['vertices']){
                //add a array for vertex neighbors for easy access
                v['neighbors'] = new Array();
                for (let n of this.graphService.GetNeighbors(this.graphData['graph'], v)){
                  v['neighbors'].push(this.graphService.FindVertex(this.graphData['graph']['vertices'],n));
                };
              }



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
  AddVertex(vData){
    //vData doesn't need id;
    //vData MUST be in the form of a vertex object
    let vertices = this.graphData['graph']['vertices'];
    let newID = this.graphService.HighestID(vertices) + 1;

    vData['id'] = newID;
    vertices.push(vData);
    this.graphData['graph']['vertices'] = vertices;

  }
  DeleteVertex(vID){
    let vertices = this.graphData['graph']['vertices'];
    let edges = this.graphData['graph']['edges'];
    let vertexIndex = vertices.indexOf(this.graphService.FindVertex(vertices,vID));

    if (vertexIndex != -1){
      //first delete any edges attached to this vertex
      console.log('Deleting any Edges that hold this vertex');
      let e = this.graphService.FindEdgeByVertexID(edges,vID);
      while (e != null){
        this.DeleteEdge(e['id']);
        e = this.graphService.FindEdgeByVertexID(edges,vID);
      }
      //then delete the vertex itself
      console.log('Splicing vertices at ' + vertexIndex);
      vertices.splice(vertexIndex,1);
      //set the new vertices since idk if its a pointer
      this.graphData['graph']['vertices'] = vertices;
    } else {
      console.log("Couldn't find " + vID + " in vertices");
    }

  }
  EditVertex(vData){
    //vData needs ID
    //vData MUST be in the form of a vertex object
    let vertices = this.graphData['graph']['vertices'];
    let vertexIndex = vertices.indexOf(this.graphService.FindVertex(vertices,vData['id']));

    if (vertexIndex != -1){
      vertices[vertexIndex] = vData;

      this.graphData['graph']['vertices'] = vertices;
    }

  }

  AddEdge(eData){
    //eData doesn't need ID
    //eData MUST be in the form of an edge object
    let edges = this.graphData['graph']['edges'];
    let newID = this.graphService.HighestID(edges) + 1;
    //you don't have to specify id this sets it automatically
    eData['id'] = newID;
    //add the edge
    edges.push(eData);

    this.graphData['graph']['edges'] = edges;

  }
  DeleteEdge(eID){
    let edges = this.graphData['graph']['edges'];
    let edgeIndex = edges.indexOf(this.graphService.FindEdge(edges,eID));

    if (edgeIndex != -1){
      console.log('Splicing edges at ' + edgeIndex);
      edges.splice(edgeIndex, 1);
      //set the graphData edges to this new edges? (i don't know if this is a clone or a pointer)
      this.graphData['graph']['edges'] = edges;
    } else {
      console.log("Couldn't find " + eID + " in edges");
    }
    
  }
  EditEdge(eData){
    //eData needs ID
    //eData MUST be in the form of an edge object
    let edges = this.graphData['graph']['edges'];
    let edgeIndex = edges.indexOf(this.graphService.FindEdge(edges,eData['id']));

    if (edgeIndex != -1){
      edges[edgeIndex] = eData;

      this.graphData['graph']['edges'] = edges;
    }

  }

  AddClassification(cData){
    //cData doesn't need id
    //cData MUST be in the form of a classification object
    let cList = this.graphData['graph']['classifications'];
    let newID = this.graphService.HighestID(cList) + 1;
    cData['id'] = newID;

    cList.push(cData);
    this.graphData['graph']['classifications'] = cList;
    
  }
  DeleteClassification(cID){
    let cList = this.graphData['graph']['classifications'];
    let vertices = this.graphData['graph']['vertices'];
    let cIndex = cList.indexOf(this.graphService.FindClassification(cList,cID));
    if (cIndex != -1){
      //first go through any vertices with this classification and delete them
      for (let v of vertices){
        if (v['type_id'] == cID){
          this.DeleteVertex(v['id']);
        }
      }
      //then delete the classification
      console.log('Splicing cList at' + cIndex);
      cList.splice(cIndex, 1);
      
      //set the graph data to the new list since idk if its a pointer
      this.graphData['graph']['classifications'] = cList;
    } else {
      console.log("Couldn't find " + cID + " in classifications");
    }

  }
  EditClassification(cData){
    //cData requires ID
    //cData MUST be in the form of a classification object
    let cList = this.graphData['graph']['classifications'];
    let cIndex = cList.indexOf(this.graphService.FindClassification(cList,cData['id']));
    console.log(cData);
    console.log(cIndex);
    if (cIndex != -1){
      cList[cIndex] = cData;
      this.graphData['graph']['classifications'] = cList;
    }

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
