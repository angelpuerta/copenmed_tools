import { Component, EventEmitter, Input, Output } from "@angular/core";


@Component({
    selector: 'copenmed-cause-list',
    templateUrl: './cause-list.component.html'
})
export class CauseList{

    @Input()
    causes: string[] = [];
    @Input()
    sourceLabel: string = '';
    @Output()
    selectedCause: EventEmitter<string> = new EventEmitter();

    explainCause(cause:string){
        this.selectedCause.emit(cause);
    }

    
}