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

  constructor(
    private formBuilder : FormBuilder,
    private graphService : GraphService
  ) {
    this.vertexForm = this.formBuilder.group({ //used in modifying the graphData
      id : null,
      name : null,
      type : null,
      type_id : null,
      health : null,
      shape : null,
      neighbors : null, //this is saved in graphComponent and not a form Option
      notes : null
    });
    this.classForm = this.formBuilder.group({ //used in modifying the graphData
      id : null,
      name : null,
      color : null,
      count : null
    });
    this.edgeForm = this.formBuilder.group({ //used in modifying the graphData
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
  }

  AddClassification(cData){
    cData['id'] = this.graphService.HighestID(this.graphService.graphData['graph']['classifications']) + 1;
    this.graphService.AddClassification(cData);
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
  }
  EditVertex(vData){
    vData['id'] = this.id;
    this.graphService.EditVertex(vData);
  }
  DeleteVertex(vData){
    this.graphService.DeleteVertex(this.id);
}

  AddEdge(eData){
    eData['id'] = this.graphService.HighestID(this.graphService.graphData['graph']['edges']) + 1;
    this.graphService.AddEdge(eData);
  }
  EditEdge(eData){
    eData['id'] = this.id;
    this.graphService.EditEdge(eData);
  }
  DeleteEdge(eData){
    this.graphService.DeleteEdge(this.id);
  }

}
