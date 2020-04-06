import { Component, OnInit } from '@angular/core';
import { GraphService } from '../../graph.service';

@Component({
  selector: 'app-graph-webgl',
  templateUrl: './graph-webgl.component.html',
  styleUrls: ['./graph-webgl.component.css']
})
export class GraphWebglComponent implements OnInit {
  graphData;

  constructor(
    private gs : GraphService, 
  ) { }

  ngOnInit() {
    this.graphData = this.gs.graphData;
  }

}
