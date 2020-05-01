import { Component, OnInit } from '@angular/core';
import { GraphService } from '../../graph.service';

import * as PIXI from 'pixi.js';
import * as UI from './UI/UI';
import { MaxLengthValidator } from '@angular/forms';

@Component({
  selector: 'app-graph-webgl',
  templateUrl: './graph-webgl.component.html',
  styleUrls: ['./graph-webgl.component.css']
})

export class GraphWebglComponent implements OnInit {
  app; loader; ticker; objects; //used in PIXI
  graphData;

  constructor(
    private gs : GraphService, 
  ) {
    
  }

  ngOnInit() {
    this.graphData = this.gs.graphData; //retrieve graphdata from service
    console.log("GraphData:");
    console.log(this.graphData);

    //initialize webGL
    this.app = new PIXI.Application({
      width: 900,
      height: 900,
      antialias: true,
      transparent : false,
      resolution: 1,
      sharedTicker: true,
    });
    let renderer = this.app.renderer;

    renderer.autoResize = true;
    
    //add to our component
    document.getElementById("display").appendChild(this.app.view);

    //load all images and run setup() when done
    this.loader = new PIXI.Loader();
    this.ticker = PIXI.Ticker.shared;
    this.ticker.autoStart = false;
    this.ticker.stop();

    this.objects = { //contains all objects
      vertices : {},
      edgeRenderer : new PIXI.Graphics()
    };
    //load all images. stack .add()s for more images
    this.loader
      .add('vertex', "assets/images/png/Vertex.png")
      .add('BG', "assets/images/png/Window/BG.png");
      //.add('Close', "assets/images/png/Window/Close.png");

    //runs after all images are loaded
    this.loader.load(
        (loader, resources) => {

          //add a vertex object for every vertex in "vertices"
          for (let vertex of this.graphData.graph.vertices){
            //create a new Sprite with the loader's vertex texture
            this.objects['vertices'][vertex.id] = new PIXI.Sprite(resources.vertex.texture);
            //add it to the stage
            this.app.stage.addChild(this.objects['vertices'][vertex.id]);
            //stuff for each individual vertex
            let v = this.objects['vertices'][vertex.id];
            v.x = Math.floor(Math.random() * this.app.renderer.width - 10);
            v.y = Math.floor(Math.random() * this.app.renderer.height - 10);
            v.tint *= Math.random();

            v.interactive = true //allows for interaction events
            v.buttonMode = true //cursor appears when you put the mouse over it
            v.anchor.set(0.5); //set the anchor point

            v.windows = { //we store windows in this object, each window has the actual 'displayObject' and additional mini settings
              node_info : new UI.Vertex_Window(resources, vertex, vertex.id + "_node_info", 32, -64, 100, 200)
            };

            //setup onclickevents for the vertex
            v
              .on('pointerdown', onDragStart)
              .on('pointerup', onDragEnd)
              .on('pointerupoutside', onDragEnd)
              .on('pointermove', onDragMove)
              .on('pointertap', onTap);

            //definitions for actual events
            function onDragStart(event){
              //store a reference the the specific data when using multitouch
              this.data = event.data;
              this.dragging = true;
            }
            function onDragEnd(){
              this.dragging = false;
              this.data = null; //set the multitouch data to null
            }
            function onDragMove(){
              if (this.dragging){
                this.moved = true;
                const newPosition = this.data.getLocalPosition(this.parent); //get the position of the mouse
                //update object's position with the new x and y
                this.x = newPosition.x;
                this.y = newPosition.y;

              }
            }

            function onTap(){ //called when the node is simply tapped/clicked
              if (this.moved == false){ //the node was not moved at all
                //we want to show node settings
                //the way we'll do this is actually set a flag for this specific node
                //and the windowrenderer will render a window based on the specific sprite
                if (this.renderSettings){
                  this.renderSettings = false;
                } else {
                  this.renderSettings = true;
                }

              } else {
                this.moved = false;
              }
            }

            //create a child Text Object of the vertex
            let t = new PIXI.Text(vertex.name,{
              fontFamily : 'Arial',
              fontSize : 12,
              fill : 0xFFFFFF
            });
            v.addChild(t);
            //set the text offset properly
            t.setTransform(-(t.width/2) + (v.width/16), v.height/2);

          } //end of vertex code

          //add the renderers
          this.app.stage.addChild(this.objects['edgeRenderer']); //add the edgeRenderer to the screen
          //add buttons


          console.log(this.objects);
          console.log(this.app.stage);

          this.ticker.start(); //actually start the ticker rendering
        } //end of loader code
      );

    
    this.ticker.add( //everything in here is called every tick
      (time) => {
        let e = this.objects['edgeRenderer'];
        e.clear();

        this.app.renderer.render(this.app.stage); //update to clear the edges

        //edge-redraw code
        for (let edge of this.graphData.graph.edges){  //go through every edge for every node
          let v1 = this.objects['vertices'][edge.vertex1_id];
          let v2 = this.objects['vertices'][edge.vertex2_id];

          //console.log(e);
          //draw edges like a pen, lifting at every node.
          e.lineStyle(2,0xFFFFFF);
          e.beginFill(0xFFFFFF);
          e.moveTo(v1.x,v1.y);
          e.lineTo(v2.x,v2.y);
          e.endFill();
        
        }
        //end of edge-redraw code

        //window drawing code
        for (let vertex of this.graphData.graph.vertices){ //loop thru the graphData's vertices
          let v = this.objects['vertices'][vertex.id]; //to get the stage's vertices
          if (v.renderSettings){ //if a vertex's renderSettings flag is on
            
            //if the node info window is not in the stage
            if (v.getChildByName(vertex.id + "_node_info") == null) {
              //update x and y before adding to stage
              let info = v.windows['node_info'];
              info.draw();
              
              v.addChild(info.container); //add it, rendering it
            } else { //if the info window is already in the stage
              let info = v.windows['node_info'];
              info.draw();
            }

          } else {
            if (v.getChildByName(vertex.id + "_node_info") != null) {
              v.removeChild(v.windows['node_info'].container);
            }
          }
        }
        

        this.app.renderer.render(this.app.stage); //call a second render to reedraw everything
        this.ticker.update(time);
      }
    );
    
  }

}
