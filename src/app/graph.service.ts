import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class GraphService {

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

}
