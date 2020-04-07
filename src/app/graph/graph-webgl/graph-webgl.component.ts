import { Component, OnInit } from '@angular/core';
import { GraphService } from '../../graph.service';

import * as PIXI from 'pixi.js';
import { MaxLengthValidator } from '@angular/forms';

@Component({
  selector: 'app-graph-webgl',
  templateUrl: './graph-webgl.component.html',
  styleUrls: ['./graph-webgl.component.css']
})

export class GraphWebglComponent implements OnInit {
  app; loader; sprites; //used in PIXI
  graphData;

  constructor(
    private gs : GraphService, 
  ) {
    
  }

  ngOnInit() {
    this.graphData = this.gs.graphData; //retrieve graphdata from service

    //initialize webGL
    this.app = new PIXI.Application({
      width: 256,
      height: 256,
      antialias: true,
      transparent : false,
      resolution: 1,
    });

    this.app.renderer.autoResize = true;

    //add to our component
    document.getElementById("display").appendChild(this.app.view);

    //load all images and run setup() when done
    this.loader = new PIXI.Loader();
    this.sprites = {};
    //load all images. stack .add()s for more images
    this.loader.add('vertex', "assets/images/png/Vertex.png");

    //runs after all images are loaded
    this.loader.load(
        (loader, resources) => {
          //add a vertex for every vertex in "vertices"
          for (let vertex of this.graphData.graph.vertices){
            this.sprites['vertex_' + vertex.id] = new PIXI.Sprite(resources.vertex.texture);
            this.app.stage.addChild(this.sprites['vertex_' + vertex.id]);
            let v = this.sprites['vertex_' + vertex.id];

            v.width *= 0.5;
            v.height *= 0.5;

            v.x = Math.floor(Math.random() * this.app.renderer.width - 10);
            v.y = Math.floor(Math.random() * this.app.renderer.height - 10);

            v.tint *= Math.random();
          }
          console.log(this.sprites);
        }
      );

  }

}
