import { Component, Input } from "@angular/core";
import { Edge, Explanation, Node } from "src/app/models/graphs";

@Component({
    selector: 'copenmed-explain-cause',
    templateUrl: './explain_cause.component.html',
    styleUrls: ['./explain_cause.component.scss']
})
export class ExplainCause{

   @Input()
   explanation!: Explanation

   @Input()
   nodes!: {[node: number]: Node}

   @Input()
   edges!: Edge[]

   panelOpenState = false;

   get target(){
    return this.translateNode(this.explanation.target);
   }

   get weight(){
       return this.explanation.weight;
   }

   get paths(){
       return this.explanation.path;
   }

   public translateNode(node:number):string {
       return this.nodes[node].label;
   }

   public translateEdges(source:number, target:number):Edge {
    const edge = this.edges.find(edge => edge.source === source && edge.target === target );
    if(edge === undefined){
        throw new Error("Edege not found");
    }
    return edge;
}

}
    