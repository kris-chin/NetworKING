import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class GraphService {

  graphData;

  constructor() { }

  //goes through a list of classification objects and returns the one with the matching id
  //returns classification object
  FindClassification(classificationList, id){
    for (let c of classificationList){
      if (c['id'] == id){
        return c;
      }
    }
    return null;
  }

  //goes through a list of vertex objects and returns the one with the matching id
  //returns vertex object
  FindVertex(vertexList, id){
    for (let v of vertexList){
      if (v['id'] == id){
        return v;
      }
    }
    return null;
  }

  //goes through a list of edge objects and returns the one with the matching id
  //returns edge object
  FindEdge(edgeList, id){
    for (let e of edgeList){
      if (e['id'] == id){
        return e;
      }
    }
    return null;
  }

  //goes through a list of edge objects and returns the one with a matching vertex id
  //returns edge object
  FindEdgeByVertexID(edgeList, vertex_id){
    for (let e of edgeList){
      if ( (e['vertex1_id'] == vertex_id) || (e['vertex2_id'] == vertex_id) ){
        return e;
      }
    }
    return null;
  }

  //returns the highest ID in a list
  HighestID(list){
    let highestValue = 0
    for (let item of list){
      try {
        if (item['id'] > highestValue){
          highestValue = item['id'];
        }
      } catch {
        console.error("HighestID(): Input list objects not all have id values");
        highestValue = null;
      }
    }
    return highestValue;
  }

  //returns a list of vertex IDs that are neighbors to given vertex in graphdata
  GetNeighbors(graph,vertexObject){
    let neighborIDList: number[] = [];
    for (let e of graph['edges']){
      if (e['vertex1_id'] == vertexObject['id']){
        if (!neighborIDList.includes(e['vertex2_id'])){
          neighborIDList.push(e['vertex2_id']);
        }
      } else if (e['vertex2_id'] == vertexObject['id']) {
        if (!neighborIDList.includes(e['vertex1_id'])){
          neighborIDList.push(e['vertex1_id']);
        }
      }
    }
    return neighborIDList;
  }

  //the following are simple actions to modify the graph
  AddVertex(vData){
    //vData doesn't need id;
    //vData MUST be in the form of a vertex object
    let vertices = this.graphData['graph']['vertices'];
    let newID = this.HighestID(vertices) + 1;

    vData['id'] = newID;
    vertices.push(vData);
    this.graphData['graph']['vertices'] = vertices;

  }
  DeleteVertex(vID){
    let vertices = this.graphData['graph']['vertices'];
    let edges = this.graphData['graph']['edges'];
    let vertexIndex = vertices.indexOf(this.FindVertex(vertices,vID));

    if (vertexIndex != -1){
      //first delete any edges attached to this vertex
      console.log('Deleting any Edges that hold this vertex');
      let e = this.FindEdgeByVertexID(edges,vID);
      while (e != null){
        this.DeleteEdge(e['id']);
        e = this.FindEdgeByVertexID(edges,vID);
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
    let vertexIndex = vertices.indexOf(this.FindVertex(vertices,vData['id']));

    if (vertexIndex != -1){
      vertices[vertexIndex] = vData;

      this.graphData['graph']['vertices'] = vertices;
    }

  }

  AddEdge(eData){
    //eData doesn't need ID
    //eData MUST be in the form of an edge object
    let edges = this.graphData['graph']['edges'];
    let newID = this.HighestID(edges) + 1;
    //you don't have to specify id this sets it automatically
    eData['id'] = newID;
    //add the edge
    edges.push(eData);

    this.graphData['graph']['edges'] = edges;

  }
  DeleteEdge(eID){
    let edges = this.graphData['graph']['edges'];
    let edgeIndex = edges.indexOf(this.FindEdge(edges,eID));

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
    let edgeIndex = edges.indexOf(this.FindEdge(edges,eData['id']));

    if (edgeIndex != -1){
      edges[edgeIndex] = eData;

      this.graphData['graph']['edges'] = edges;
    }

  }

  AddClassification(cData){
    //cData doesn't need id
    //cData MUST be in the form of a classification object
    let cList = this.graphData['graph']['classifications'];
    let newID = this.HighestID(cList) + 1;
    cData['id'] = newID;

    cList.push(cData);
    this.graphData['graph']['classifications'] = cList;
    
  }
  DeleteClassification(cID){
    let cList = this.graphData['graph']['classifications'];
    let vertices = this.graphData['graph']['vertices'];
    let cIndex = cList.indexOf(this.FindClassification(cList,cID));
    if (cIndex != -1){
      //first go through any vertices with this classification and delete them
      
      //for some reason not all the vertices delete when simply looping through all vertices,
      //so we'll just save the id's of the affected vertices and delete them manually
      let affectedVertices = new Array();
      for (let v of vertices){if (v['type_id'] == cID) {affectedVertices.push(v['id']);}}
      for (var i = 0; i < affectedVertices.length; i++){this.DeleteVertex(affectedVertices[i]);}
      
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
    let cIndex = cList.indexOf(this.FindClassification(cList,cData['id']));
    console.log(cData);
    console.log(cIndex);
    if (cIndex != -1){
      cList[cIndex] = cData;
      this.graphData['graph']['classifications'] = cList;
    }

  }

}
