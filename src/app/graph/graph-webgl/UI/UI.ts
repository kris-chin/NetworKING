import * as PIXI from 'pixi.js'
import { GraphService } from '../../../graph.service';

export class Window {
    container; bg;
    x_offset; y_offset

    constructor(loadedResources, name, x_offset, y_offset, width, height){
        //loadedResources refers to the PIXI loader's resources once all textures are loaded
        this.container = new PIXI.Container();
        this.bg = new PIXI.Sprite(loadedResources.BG.texture);
        
        //if the host object IS null, the x and y offset become the actual coordinates
        this.x_offset = x_offset;
        this.y_offset = y_offset;

        this.container.name = name;
        this.bg.width = width;
        this.bg.height = height;

        this.container.addChild(
            this.bg //BG sprite (to scale the window)
            //close //Close Button
        );

    }

    draw(){ //draw function called on every ticker
        this.container.x = this.x_offset;
        this.container.y = this.y_offset;
    }

}

export class Vertex_Window extends Window{
    tO = { //text objects
        name : null,
        type : null,
        neighbors : null
    };

    constructor(loadedResources, vertex_object, name, x_offset, y_offset, width, height){
        
        //super calls the parent's constructor! whoa!
        super(loadedResources, name, x_offset, y_offset, width, height);
        
        //create the string of all of the neighbors
        let neighborString = "Neighbors:\n";
        for (let n of vertex_object.neighbors){
            neighborString += n.name + "\n";
            
        }

        this.tO = {
            name: new PIXI.Text("Name:\n" + vertex_object.name,{
              fontFamily : 'Arial',
              fontSize : 12,
              fill : 0xFFFFFF
            }),

            type: new PIXI.Text("Type:\n" + vertex_object.type, {
              fontFamily : 'Arial',
              fontSize : 12,
              fill : 0xFFFFFF
            }),

            neighbors: new PIXI.Text(neighborString, {
                fontFamily : 'Arial',
                fontSize : 12,
                fill : 0xFFFFFF
              })
        };

        this.container.addChild(
            this.tO['name'],
            this.tO['type'],
            this.tO['neighbors']
        )

        //autoclose if window is clicked (to avoid missing other vertices)
        this.container.interactive = true;
        this.container
            .on('pointertap', onTap);

        function onTap(){
            //remove the container by itself
            
        }
        

    }

    draw(){ //draw function called on every ticker

        this.container.x =0;
        this.container.y =0;

        //note: all child objects of the container have their x and y relative to the container 

        this.tO['name'].x = 20;
        this.tO['name'].y = 0;

        this.tO['type'].x = 20;
        this.tO['type'].y = 40;

        this.tO['neighbors'].x = 20;
        this.tO['neighbors'].y = 80;

    }


}