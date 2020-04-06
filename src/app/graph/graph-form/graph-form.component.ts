import { Component, OnInit, Input } from '@angular/core';
import { FormBuilder, FormControl} from '@angular/forms';
import { GraphService } from '../../graph.service';

@Component({
  selector: 'app-graph-form',
  templateUrl: './graph-form.component.html',
  styleUrls: ['./graph-form.component.css']
})
export class GraphFormComponent implements OnInit {
  @Input() formType : string;
  @Input() id : any;
  @Input() action : any;
  vertexForm; classForm; edgeForm;
  graphData;

  constructor(
    private formBuilder : FormBuilder,
    private graphService : GraphService
  ) {
    this.vertexForm = this.formBuilder.group({ //used in modifying the graphData
      id : null,
      name : '',
      type : null,
      type_id : null,
      health : 1,
      shape : 'o',
      neighbors : null, //this is saved in graphComponent and not a form Option
      notes : ''
    });
    this.classForm = this.formBuilder.group({ //used in modifying the graphData
      id : null,
      name : '',
      color : 'black',
      count : 0
    });
    this.edgeForm = this.formBuilder.group({ //used in modifying the graphData
      id : null,
      name : '',
      vertex1 : null,
      vertex1_id : null,
      vertex2 : null,
      vertex2_id : null,
      color : 'Black',
      size : 1,
      style : 'solid'
    });
  }

  //used in type dropdown for adding/changing a vertex
  changeType(t){
    this.vertexForm['type_id'].setValue(t.id, {onlySelf: true});
  }

  ngOnInit() {
    //set default values
    if (this.action == 'EditClass'){
      let cList = this.graphService.graphData['graph']['classifications'];
      this.classForm.setValue(this.graphService.FindClassification(cList,this.id));
    } else if (this.action == 'EditVertex'){
      let vList = this.graphService.graphData['graph']['vertices'];
      this.vertexForm.setValue(this.graphService.FindVertex(vList,this.id));
    } else if (this.action == 'EditEdge'){
      let eList = this.graphService.graphData['graph']['edges'];
      this.edgeForm.setValue(this.graphService.FindEdge(eList,this.id));
    } 

    this.graphData = this.graphService.graphData;
  }

  AddClassification(cData){
    cData['id'] = this.graphService.HighestID(this.graphService.graphData['graph']['classifications']) + 1;
    this.graphService.AddClassification(cData);
    this.classForm.reset({
      name : '',
      color : 'black',
      count : 0
    });
  }
  EditClassification(cData){
    cData['id'] = this.id;
    this.graphService.EditClassification(cData);
  }
  DeleteClassification(cData){
    this.graphService.DeleteClassification(this.id);
  }

  AddVertex(vData){
    vData['id'] = this.graphService.HighestID(this.graphService.graphData['graph']['vertices']) + 1; 
    this.graphService.AddVertex(vData);
    this.vertexForm.reset({
      name : '',
      health : 1,
      shape : 'o',
      notes : ''
    });
  }
  EditVertex(vData){
    vData['id'] = this.id;
    this.graphService.EditVertex(vData);
  }
  DeleteVertex(vData){
    this.graphService.DeleteVertex(this.id);
}

  AddEdge(eData){
    if (this.action == 'AddNeighbor'){
      let vList = this.graphData['graph']['vertices'];
      eData['vertex1'] = this.graphService.FindVertex(vList, this.id)['name'];
      eData['vertex1_id'] = this.id;
    }

    eData['id'] = this.graphService.HighestID(this.graphService.graphData['graph']['edges']) + 1;
    this.graphService.AddEdge(eData);
    this.edgeForm.reset({
      name : '',
      color : 'Black',
      size : 1,
      style : 'solid'
    });
  }
  EditEdge(eData){
    eData['id'] = this.id;
    this.graphService.EditEdge(eData);
  }
  DeleteEdge(eData){
    this.graphService.DeleteEdge(this.id);
  }

}
